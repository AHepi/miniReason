# Working answer

The unique left-to-right order is D, A, F, E, C, G, B, occupying slots 1 through 7 respectively. Let a be the slot of A. Then A=a, F=a+1, C=a+3, and G=a+4, so a<=3. If a=1, then G=5 and B is 6 or 7. If B=6, span(A,B)=6, requiring |D-5|+1=6, so |D-5|=5, impossible. If B=7, span(A,B)=7, requiring |D-5|=6, also impossible. If a=2, then A=2, F=3, C=5, G=6, and B must be 7. Then span(A,B)=|2-7|+1=6, so span(D,G)=|D-6|+1=6, giving D=1. The remaining slot 4 is E. This yields D, A, F, E, C, G, B and satisfies all rules. If a=3, then G=7, but B must be after G, impossible. Therefore the order is unique.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `no_new_objections`. Read TRACE.md for open objections.
