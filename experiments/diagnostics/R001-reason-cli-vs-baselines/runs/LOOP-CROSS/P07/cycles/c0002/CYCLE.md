# Cycle 2

Working answer after return:

All arithmetic is modulo 19.

1) f is not one-to-one. For example, f(3)=27+24=51≡13 (mod 19), while f(5)=125+40=165≡13 (mod 19), and 3≠5.

2) The possible original inputs that give recorded encoded residue 13 are {3,5,11}. Check: f(3)=51≡13, f(5)=165≡13, and f(11)=1331+88=1419≡13, since 19*74=1406. The polynomial x^3+8x-13 has degree 3 over the field Z/19Z, so it has at most three roots; the three distinct roots found are therefore all of them.

3) Value table x -> f(x) for x=0,...,18:
0->0, 1->9, 2->5, 3->13, 4->1, 5->13, 6->17, 7->0, 8->6, 9->3, 10->16, 11->13, 12->0, 13->2, 14->6, 15->18, 16->6, 17->14, 18->10.
The output set is {0,1,2,3,5,6,9,10,13,14,16,17,18}. Therefore the residues this device can never output are {4,7,8,11,12,15}.

4) d(x)=3x^2+8 is nonzero for every allowed x. If d(x)=0, then 3x^2+8≡0, so 3x^2≡11. Since 3^{-1}≡13 because 3*13=39≡1, this gives x^2≡11*13=143≡10. The quadratic residues modulo 19 are the squares 0^2 through 9^2: {0,1,4,9,16,6,17,11,7,5} = {0,1,4,5,6,7,9,11,16,17}. The value 10 is not among them, so x^2≡10 has no solution modulo 19. Hence d(x) is nonzero for every x in {0,...,18}.

The objections claiming d(7)=0 and d(12)=0 are based on a false congruence. Actually 7^2=49 and 19*2=38, so 49≡11 (mod 19), not 10. Thus d(7)=3*49+8=155≡3 (mod 19), not 0. Also 12^2=144 and 19*7=133, so 144≡11 (mod 19), and d(12)=3*144+8=440≡3 (mod 19), not 0. The statement 49=2*19+10 is also false because 2*19+10=48.

Use question:

Does the formal derivative d(x) = 3x^2 + 8 evaluate to zero modulo 19 when x = 7?

Independent derivation from PROBLEM:

To determine if d(7) is zero, I calculate 3*(7^2) + 8 modulo 19. First, 7^2 = 49. Dividing 49 by 19 gives 2 with a remainder of 11 (since 19*2 = 38 and 49-38=11). Thus, 7^2 ≡ 11 (mod 19). Next, substitute this into the expression: 3*11 + 8 = 33 + 8 = 41. Finally, reduce 41 modulo 19: 19*2 = 38, and 41 - 38 = 3. Therefore, d(7) ≡ 3 (mod 19), which is not zero.

Derivation from WORKING ANSWER:

The WORKING ANSWER claims that d(x) is nonzero for every allowed x. Specifically, it addresses the check at x=7 by stating: '7^2=49≡11, not 10, so d(7)=3*49+8=155≡3 (mod 19), not 0'. This derivation relies on the claim that 7^2 ≡ 11 (mod 19) and concludes that d(7) = 3.

Dispositions and new use objections:

```json
{
  "dispositions": [
    {
      "id": "c0001-k01-o001",
      "status": "rejected-with-reason",
      "reason": "The objection's arithmetic is false: 49=2*19+11, not 2*19+10, so 7^2≡11 (mod 19), not 10. The listed quadratic residues {0,1,4,5,6,7,9,11,16,17} correctly omit 10, so x^2≡10 has no solution. The derivative conclusion d(x) nonzero for every allowed x is not invalidated."
    },
    {
      "id": "c0001-k01-o002",
      "status": "rejected-with-reason",
      "reason": "This objection depends on the false congruences 7^2≡10 and 12^2≡10. In fact 7^2≡11 and 12^2≡11 modulo 19, so d(7)=155≡3 and d(12)=440≡3, not 0. The derivative equation reduces to x^2≡10, which has no solution modulo 19; therefore d(x) is nonzero at every allowed x."
    }
  ],
  "use_objections": []
}
```

Exact requests and responses: ../../calls/c0002-*

## Visible working: c0002-k01/a00

Re-verified the core arithmetic disputed in prior objections. The claim that 7^2 ≡ 10 (mod 19) is false; 7^2 = 49 = 2*19 + 11, so 7^2 ≡ 11. Consequently, d(7) = 3(11) + 8 = 41 ≡ 3 (mod 19), which is non-zero. The set of quadratic residues modulo 19 is {0, 1, 4, 5, 6, 7, 9, 11, 16, 17}, confirming 10 is not a residue. The working answer's derivation that x^2 ≡ 10 has no solution and thus d(x) is never zero is correct. No new specific errors are found in the value table or the one-to-one counterexamples.


## Visible working: c0002-k02/a00

I independently verified each part. Recomputing f(x)=x^3+8x mod 19 for all x=0..18 gives exactly the table shown (e.g. f(7)=343+56=399=19*21 -> 0; f(12)=1728+96=1824=19*96 -> 0; f(16)=4096+128=4224, 4224-4218=6), so the output set {0,1,2,3,5,6,9,10,13,14,16,17,18} and never-output list {4,7,8,11,12,15} are correct. The preimage of 13 is confirmed as {3,5,11} by the degree-3 root bound, and Vieta checks agree: 3+5+11=19=0, pairwise products 15+33+55=103=8, product 165=13. For d(x), d(x)=0 forces 3x^2=11, so x^2=11*13=143=10; the nonzero squares mod 19 are {1,4,5,6,7,9,11,16,17}, and 10 is a non-residue (e.g. (2/19)=-1, (5/19)=1, so (10/19)=-1), so d(x) is never zero; direct checks like d(7)=155=3 and d(12)=440=3 confirm. Both prior objections hinged on the false congruence 7^2=10 (actually 49-38=11), and their dispositions are arithmetically sound. The non-injectivity counterexample f(3)=f(5)=51=165=13 is correct. I found no remaining error.

