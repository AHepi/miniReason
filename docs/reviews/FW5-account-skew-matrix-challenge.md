# An attempted Account counterexample: odd-order skew-symmetric matrices

Result: the proposed sufficiency counterexample fails. The candidate calculation satisfies the declared structural conditions, but its supposed absence of explanatory bearing does not survive independent examination. This rejects one attempted witness; it neither confirms FW5 nor settles other sufficiency and necessity attacks.

The target is the designated [FW5 reading edition](../sources/FW5-explanatory-construction.md), specifically “A structural answer,” equation (E), and “A structural account that still does not explain.” The source explicitly distinguishes adequacy to a stated mathematical question from the deepest or most illuminating account. The candidate was chosen before symbolic checking, as recorded in REC-20260912-G. An independent agent constructed and criticized the case; root reviewed the argument and reproduced the exact arithmetic. No provider or Mini run occurred.

## Frozen question and organization

The question is: **Why must every odd-order real skew-symmetric matrix be singular, independently of its entries?** The respect is mathematical obstruction, with scope over all finite odd dimensions and all real entries consistent with skew-symmetry. It is not changed afterward into a question about a single computed determinant.

The grain retains dimension, individual matrix entries, skewness constraints, determinant products and sums, and their algebraic dependencies. The boundary fixes real-field arithmetic and the equivalence between invertibility and nonzero determinant. The target organization contains the matrix constraints and determinant relation. This is a mathematical case; no causal intervention on a physical matrix is claimed.

Admitted contrasts remove the skew-symmetry constraint, remove the restriction to odd dimension, or remove both, while preserving field arithmetic and the determinant/invertibility interpretation. These are deletions of independent restrictions on the matrix family. Their identity and composition maps agree; the two removals commute. The explanatory organization uses the general determinant expansion under each resulting family, so the contrast does not reuse an odd-skew cancellation premise where that premise no longer applies.

## Candidate adverse account

For an n-by-n matrix A, expand the determinant by the Leibniz formula

\[
\det A=\sum_{\pi\in S_n}\operatorname{sgn}(\pi)\prod_{i=1}^{n}a_{i,\pi(i)}.
\]

Substitute the stipulated skewness relations and collect the polynomial terms. This produces zero for arbitrary entries in the odd-dimensional family. The attempted attack called this an exhaustive calculation rather than an explanation: it can be enormous and does not initially foreground the short transpose/parity invariant.

The adverse proposal concerns this uniform symbolic algorithm and its dependencies, not a finite table of successful numerical examples. The target determinant-zero assertion is never inserted as a premise. Arbitrary-entry cancellation and its general justification are the crucial facts to assess.

## Account assessment

| FW5 conjunct | Interpretation and assessment |
|---|---|
| Anchoring | Entry ports, skew constraints, dimension, multiplication, addition and determinant terms retain their literal mathematical roles. Each derived term or sum expands a specified determinant suborganization; projecting away intermediate ports yields its anchored relation. No empirical association is substituted for a causal or constitutive relation. |
| Fidelity, including composition | Adding uniquely determined intermediate products/sums and then projecting them away preserves the same matrix/determinant valuations. This holds in the odd-skew family and under each declared restriction removal. Identity and the commuting restriction-removal compositions are preserved. |
| Question fidelity | The answer remains the absence of invertible matrices in the entire stipulated odd-skew family, independent of entries. Under the contrasts, the family can contain invertible matrices. The account addresses the original obstruction respect; it is not restricted to checked numerical instances. |
| Non-circular dependence | The zero result follows from expansion and cancellation with real arithmetic. Removing skewness admits the odd-dimensional identity matrix I3, determinant 1. Removing oddness admits the two-dimensional skew matrix with rows (0,1) and (-1,0), determinant 1. These change substantive constraints while preserving the other boundary assumptions. |
| Non-vacuity | Compatible odd-dimensional skew matrices exist; the check includes a nonzero 3-by-3 example. Baseline consistency is distinct from the impossibility of achieving invertibility within that family. |

This is a substantive interpretation of the argument, not a checker-generated semantic verdict. In particular, fidelity does not follow from testing two dimensions; it follows from expansion of the determinant's defining relation and the stated projection.

## Independent examination of the alleged absence of bearing

A determinant term whose permutation has a fixed point vanishes because a diagonal entry of a real skew-symmetric matrix is zero. Every remaining permutation pairs with its inverse. Their permutation signs agree. Reindexing the inverse term and using skewness reverses every matrix factor, giving an overall factor of (-1)^n. For odd n the two terms therefore cancel.

The pairing has no unpaired fixed-point-free permutation. A permutation equal to its inverse is an involution. An involution without fixed points partitions its indices into pairs, so its dimension must be even. Thus in odd dimension the inverse permutation is distinct, and every surviving term belongs to a cancelling pair.

The calculation consequently contains the relevant organization: skewness reverses an odd number of factors, and parity prevents a surviving unpaired term. The cancellation is an obstruction argument. The shorter proof

\[
\det A=\det A^{T}=\det(-A)=(-1)^n\det A
\]

makes the same obstruction easier to see, but relative clarity does not establish that the expansion has no bearing. Over the reals, odd n then gives 2 det A = 0 and hence det A = 0. This reasoning would need separate consideration over a field of characteristic two; that field is outside this frozen contract and is not quietly absorbed into it.

The attempted independent absence-of-bearing argument therefore fails. Reclassifying the calculation as non-explanatory solely because it is less elegant would import an additional criterion that the stated FW5 target does not assert. This conclusion is local to the explicitly reconstructed candidate. It is not the claim that every computation or every valid proof explains every why-question.

## Reproducible checking and limits

[check.py](../../experiments/diagnostics/fw5-account-skew-matrix/check.py) uses exact integer coefficients and symbolic monomials. At dimension three it finds two nonzero terms before collection, which cancel. At dimension five it finds forty-four nonzero terms, collecting into twenty-two cancelling monomials. No numerical sampling approximates these identities. The script also checks the two determinant-one contrast witnesses and a compatible nonzero odd-skew baseline.

[result.json](../../experiments/diagnostics/fw5-account-skew-matrix/result.json) preserves the exact output. [run.json](../../experiments/diagnostics/fw5-account-skew-matrix/run.json) records root's reproduction, script/output hashes and zero provider calls. Run from repository root with `python experiments/diagnostics/fw5-account-skew-matrix/check.py`.

The finite checks establish the stated dimension-three and dimension-five polynomial identities and the explicit contrast witnesses. The all-odd-dimension conclusion rests on the separate permutation argument above. Neither establishes Account's constitutive adequacy. This is an authored mathematical case, not the requested future challenge to an independently sourced interpretive technical document.

The next theory-side search needs an independent non-bearing argument that survives the complete organization, original respect and active dependencies. This failed candidate supplies no such argument. Cases involving interpretive scope, genuine inexplicit understanding or the Account-to-epistemic-obligation connection remain open. A failed parser, a less readable proof, or an arbitrary change of grain cannot stand in for that missing case.
