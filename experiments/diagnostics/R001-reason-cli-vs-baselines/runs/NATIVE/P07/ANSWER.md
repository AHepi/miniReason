# Working answer

All arithmetic is modulo 19.

1) f is not one-to-one. For example, f(3)=27+24=51≡13 (mod 19), while f(5)=125+40=165≡13 (mod 19), and 3≠5.

2) The possible original inputs that give recorded encoded residue 13 are {3,5,11}. Check: f(3)=51≡13, f(5)=165≡13, and f(11)=1331+88=1419≡13, since 19*74=1406. The polynomial x^3+8x-13 has degree 3 over the field Z/19Z, so it has at most three roots; the three distinct roots found are therefore all of them.

3) Value table x -> f(x) for x=0,...,18:
0->0, 1->9, 2->5, 3->13, 4->1, 5->13, 6->17, 7->0, 8->6, 9->3, 10->16, 11->13, 12->0, 13->2, 14->6, 15->18, 16->6, 17->14, 18->10.
The output set is {0,1,2,3,5,6,9,10,13,14,16,17,18}. Therefore the residues this device can never output are {4,7,8,11,12,15}.

4) d(x)=3x^2+8 is nonzero for every allowed x. If d(x)=0, then 3x^2+8≡0, so 3x^2≡11. Since 3^{-1}≡13 because 3*13=39≡1, this gives x^2≡11*13=143≡10. The quadratic residues modulo 19 are the squares 0^2 through 9^2: {0,1,4,9,16,6,17,11,7,5} = {0,1,4,5,6,7,9,11,16,17}. The value 10 is not among them, so x^2≡10 has no solution modulo 19. Hence d(x) is nonzero for every x in {0,...,18}.

The objections claiming d(7)=0 and d(12)=0 are based on a false congruence. Actually 7^2=49 and 19*2=38, so 49≡11 (mod 19), not 10. Thus d(7)=3*49+8=155≡3 (mod 19), not 0. Also 12^2=144 and 19*7=133, so 144≡11 (mod 19), and d(12)=3*144+8=440≡3 (mod 19), not 0. The statement 49=2*19+10 is also false because 2*19+10=48.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `no_new_objections`. Read TRACE.md for open objections.
