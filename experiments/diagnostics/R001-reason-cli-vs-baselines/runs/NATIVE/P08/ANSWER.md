# Working answer

Minimum total weighted completion time: 253.

Optimal order: E -> B -> D -> idle 6-7 -> F -> C -> A.

Schedule:
E start 0, complete 3;
B start 3, complete 5;
D start 5, complete 6;
idle 6 to 7;
F start 7, complete 9;
C start 9, complete 13;
A start 13, complete 18.

Objective: 2*3 + 9*5 + 7*6 + 6*9 + 4*13 + 3*18 = 6 + 45 + 42 + 54 + 52 + 54 = 253.

Global optimality proof. Let f(R,t) be the minimum additional weighted completion cost from time t with remaining set R. The exact recurrence is f(empty,t)=0 and f(R,t)=min over j in R of [ w_j*(max(t,r_j)+p_j) + f(R without j, max(t,r_j)+p_j) ]. This covers every possible next job and every necessary wait: waiting before a chosen job is represented by max(t,r_j). Since all releases and processing times are integers, an optimal schedule can be taken with integer starts, so the recurrence is exact for the real-valued statement as well.

First-job cases from t=0:
E: 2*3 + f({A,B,C,D,F},3) = 6 + 247 = 253.
A: 3*5 + f({B,C,D,E,F},5) = 15 + 264 = 279.
C: idle 0-1 then 4*5 + f({A,B,D,E,F},5) = 20 + 254 = 274.
B: idle 0-2 then 9*4 + f({A,C,D,E,F},4) = 36 + 243 = 279.
D: idle 0-5 then 7*6 + f({A,B,C,E,F},6) = 42 + 288 = 330.
F: idle 0-7 then 6*9 + f({A,B,C,D,E},9) = 54 + 352 = 406.
So no first job other than E can beat 253.

For E first:
f({A,B,C,D,F},3) = min(
 B: 9*5 + f({A,C,D,F},5) = 45 + 202 = 247,
 C: 4*7 + f({A,B,D,F},7) = 28 + 269 = 297,
 A: 3*8 + f({B,C,D,F},8) = 24 + 308 = 332,
 D: 7*6 + f({A,B,C,F},6) = 42 + 245 = 287,
 F: 6*9 + f({A,B,C,D},9) = 54 + 305 = 359
) = 247.

f({A,C,D,F},5) = min(
 D: 7*6 + f({A,C,F},6) = 42 + 160 = 202,
 C: 4*9 + f({A,D,F},9) = 36 + 193 = 229,
 A: 3*10 + f({C,D,F},10) = 30 + 223 = 253,
 F: 6*9 + f({A,C,D},9) = 54 + 183 = 237
) = 202.

f({A,C,F},6) = min(
 F: 6*9 + f({A,C},9) = 54 + 106 = 160,
 C: 4*10 + f({A,F},10) = 40 + 123 = 163,
 A: 3*11 + f({C,F},11) = 33 + 146 = 179
) = 160.

The all-available subproblems use WSPT (descending w/p): f({A,C},9)=4*13+3*18=106; f({A,F},10)=6*12+3*17=123; f({C,F},11)=6*13+4*17=146; f({A,D,F},9)=7*10+6*12+3*17=193; f({C,D,F},10)=7*11+6*13+4*17=223; f({A,C,D},9)=7*10+4*14+3*19=183; f({A,B,D,F},7)=7*8+9*10+6*12+3*17=269; f({B,C,D,F},8)=7*9+9*11+6*13+4*17=308; f({A,B,C,F},6)=9*8+6*10+4*14+3*19=245; f({A,B,C,D},9)=7*10+9*12+4*16+3*21=305.

Thus the E branch is forced through B at t=3, D at t=5, then the optimal state f({A,C,F},6) is to wait for F at 7. Total 253. Since every first choice and every next-job choice is covered by the recurrence, 253 is globally minimal.

On the idle interval 6-7: F is not released until 7. Waiting and choosing F next costs 54 + f({A,C},9) = 160. Starting C at 6 costs 40 + f({A,F},10) = 163; starting A at 6 costs 33 + f({C,F},11) = 179. So waiting is not a local heuristic but the recurrence's minimum. If F were available at 6, the same recurrence would choose F at 6: 6*8 + f({A,C},8) = 48 + 99 = 147, so the idle slot is due to F's release time, not an artifact.

On the alleged propagation error: 40 + f({A,D,F},9) is not the C-option in f({A,C,F},6). It belongs to f({A,C,D,F},5), where C starts at 5 and completes at 9, leaving A,D,F at t=9. In f({A,C,F},6), starting C at 6 completes at 10, leaving {A,F} at t=10, so the correct term is 40 + f({A,F},10) = 40 + 123 = 163. The comparison 160 < 163 < 179 stands.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `cycle_budget`. Read TRACE.md for open objections.
