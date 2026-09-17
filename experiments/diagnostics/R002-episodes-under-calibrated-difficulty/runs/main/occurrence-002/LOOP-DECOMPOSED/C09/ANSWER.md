# Working answer

Accepted partial steps (no synthesis):

1. F_0(s,t)=((s+t) mod 4,(t+1) mod 3); F_1(s,t)=((2s+t+1) mod 4,(s+t) mod 3); initial state (1,0).
2. Each fixed length-12 bit string with exactly seven 1s has probability (3/5)^7(2/5)^5, independent of the positions of the 1s.
3. N_{0,0}(1,0)=1 and all other N_{0,j}(s,t)=0. For k+1>=1, N_{k+1,j}(s,t)=sum over (u,v) with F0(u,v)=(s,t) of N_{k,j}(u,v) + sum over (u,v) with F1(u,v)=(s,t) of N_{k,j-1}(u,v), over Z4 x Z3, with j ranging 0..k+1 and out-of-range terms zero.

Stop reason: `step_budget`.
