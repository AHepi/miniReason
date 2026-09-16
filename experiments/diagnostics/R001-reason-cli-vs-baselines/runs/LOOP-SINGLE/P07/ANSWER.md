# Working answer

All computations are modulo 19, with residues 0,...,18.

1. f is not one-to-one. f(3)=3^3+8·3=27+24=51≡13 (mod 19). f(5)=5^3+8·5=125+40=165≡13 (mod 19). Since 3≠5 but f(3)=f(5), f is not injective.

2. d(x)=3x^2+8 is nonzero for every allowed x. If d(x)=0, then 3x^2≡-8≡11, so x^2≡11·3^{-1}. Since 3·13=39≡1, 3^{-1}=13. Thus x^2≡11·13=143≡10 (mod 19). The quadratic residues modulo 19 are the squares of 0,...,9: 0,1,4,9,16,6,17,11,7,5, i.e. {0,1,4,5,6,7,9,11,16,17}. The value 10 is not in this set, so no x∈{0,...,18} satisfies d(x)=0. Therefore d(x) is nonzero at every allowed residue. (Nonzero derivative here does not imply f is one-to-one; indeed it is not.)

3. Preimages of 13: f(x)=13. We have f(3)=13, f(5)=13, and f(11)=11^3+8·11. Since 11^3=1331≡1 (mod 19) and 8·11=88≡12, f(11)=1+12=13. The polynomial x^3+8x-13 has degree 3 over the field mod 19, so it has at most three roots; the three distinct roots 3,5,11 are therefore all of them. Equivalently, (x-3)(x-5)(x-11)≡x^3+8x-13 (mod 19). So the original inputs giving recorded residue 13 are exactly {3,5,11}.

4. The complete output list f(0),...,f(18) is:
0,9,5,13,1,13,17,0,6,3,16,13,0,2,6,18,6,14,10.
Thus the image is {0,1,2,3,5,6,9,10,13,14,16,17,18}. The residues that can never be output are the complement in {0,...,18}: {4,7,8,11,12,15}.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `no_new_objections`. Read TRACE.md for open objections.
