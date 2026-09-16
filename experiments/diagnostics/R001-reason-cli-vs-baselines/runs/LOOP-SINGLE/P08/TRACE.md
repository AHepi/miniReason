# Objection trace

This is a personal working tool. Its output is a working answer with its objections, not a finding.

## c0001-k01-o001

Source: deepseek-flash; introduced cycle 1.

The claim 'This captures every feasible nonpreemptive schedule, because any schedule is a permutation of jobs with idle inserted exactly when the next release time exceeds the current machine completion time' is false. The problem explicitly permits idle even when a job is available. For example, idle 0–1 then E 1–4, B 4–6, C 6–10, D 10–11, F 11–13, A 13–18 is feasible, but the DP transition for E from t=0 forces start max(0,r_E)=0, not 1, so this schedule is not represented. The DP enumerates schedules with no voluntary idle before a released job, not every feasible schedule. The optimality argument needs the additional observation that such voluntary idle can be removed without worsening any completion time.

Would defeat: The claim that the subset DP captures every feasible nonpreemptive schedule and that its enumeration alone establishes global optimality.

Cycle 1: **unresolved** - New objection awaiting operative return.

Cycle 1: **taken-up** - The objection is correct about the original wording. The repair is the left-shift argument: for any feasible schedule, keep its job order and restart each job at max(previous completion, its release time). By induction every completion time is no later, so the weighted sum does not increase. Hence an optimal schedule can be chosen among earliest-start schedules, and the subset DP enumerates exactly those. The objection's example idle 0-1 then E is left-shifted to E 0-3, B 3-5, etc., with lower cost, so omitting it does not miss the global optimum. The optimal 253 schedule is unchanged.

Cycle 2: **taken-up** - The original claim that the DP enumerates every feasible schedule was too broad. The corrected argument uses left-shifting: for any feasible schedule, keep the job order and restart each job at max(previous completion, its release time). By induction every completion time is no later, so the positive-weighted sum does not increase. Hence an optimal schedule exists among earliest-start schedules, and the subset DP enumerates exactly those. The objection's example with idle 0-1 before E left-shifts to E starting at 0 with lower cost. The optimal value remains 253.

Current disposition: **taken-up** - The original claim that the DP enumerates every feasible schedule was too broad. The corrected argument uses left-shifting: for any feasible schedule, keep the job order and restart each job at max(previous completion, its release time). By induction every completion time is no later, so the positive-weighted sum does not increase. Hence an optimal schedule exists among earliest-start schedules, and the subset DP enumerates exactly those. The objection's example with idle 0-1 before E left-shifts to E starting at 0 with lower cost. The optimal value remains 253.

