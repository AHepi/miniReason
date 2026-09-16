# Working answer

Exact minimum = 253.

Schedule (order E -> B -> D -> idle -> F -> C -> A):
- E: start 0, completion 3.
- B: start 3, completion 5.
- D: start 5, completion 6.
- Idle: 6 to 7, because in this order the next job F is not released until 7.
- F: start 7, completion 9.
- C: start 9, completion 13.
- A: start 13, completion 18.

Objective check:
E: 2*3 = 6
B: 9*5 = 45
D: 7*6 = 42
F: 6*9 = 54
C: 4*13 = 52
A: 3*18 = 54
Total = 6 + 45 + 42 + 54 + 52 + 54 = 253.

Global optimality: For any fixed job order, left-shifting each job to its earliest feasible start s_j = max(previous completion, r_j) cannot increase any completion time. Hence it cannot increase the positive-weighted completion sum. Therefore an optimal schedule can be chosen among earliest-start schedules, and it is enough to minimize over all 6! orders under this earliest-start rule. The subset DP does exactly that. Its best final-job values are: final A 253, final C 261, final E 275, final F 280, final D 320, final B 348. Thus no schedule ending with another job beats 253. For final A, the relevant nondominated states before A are (t=12,c=205) and (t=13,c=199); adding A gives 256 and 253, so the latter is optimal. The idle interval 6-7 in the optimum is forced by choosing F next before its release time 7; idle before an already released next job can be removed without worsening any completion time.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `no_new_objections`. Read TRACE.md for open objections.
