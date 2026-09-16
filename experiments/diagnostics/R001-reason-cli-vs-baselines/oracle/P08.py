"""Every feasible nonpreemptive schedule has an order; earliest times dominate."""
import itertools
import json
from fractions import Fraction

JOBS = {"A": (0, 5, 3), "B": (2, 2, 9), "C": (1, 4, 4),
        "D": (5, 1, 7), "E": (0, 3, 2), "F": (7, 2, 6)}

def evaluate(order):
    now = total = 0
    rows = []
    for name in order:
        release, duration, weight = JOBS[name]
        start = max(now, release)
        now = start + duration
        total += weight * now
        rows.append([name, start, now])
    return total, rows

def solve():
    results = [(evaluate(o)[0], o) for o in itertools.permutations(sorted(JOBS))]
    minimum = min(total for total, o in results)
    optimal_orders = [o for total, o in results if total == minimum]
    assert len(results) == 720 and len(optimal_orders) == 1
    order = optimal_orders[0]
    total, rows = evaluate(order)
    remaining = set(JOBS)
    now = 0
    greedy = []
    while remaining:
        ready = [j for j in remaining if JOBS[j][0] <= now]
        if not ready:
            now = min(JOBS[j][0] for j in remaining)
            continue
        job = min(ready, key=lambda j: (Fraction(JOBS[j][1], JOBS[j][2]), j))
        greedy.append(job)
        now += JOBS[job][1]
        remaining.remove(job)
    answer = {"minimum_weighted_completion_sum": total, "order": list(order),
              "start_finish": rows, "idle_intervals": [[6, 7]]}
    assert total == 253 and order == ("E", "B", "D", "F", "C", "A")
    states = {(frozenset(), 0): (0, [])}
    for depth in range(6):
        nxt = {}
        for (done, finish), (cost, route) in states.items():
            for job in sorted(set(JOBS) - done):
                release, duration, weight = JOBS[job]
                end = max(finish, release) + duration
                key = (done | {job}, end)
                candidate = (cost + weight * end, route + [job])
                if key not in nxt or candidate[0] < nxt[key][0]:
                    nxt[key] = candidate
        states = nxt
    assert min(value[0] for value in states.values()) == total
    return {"problem_id": "P08", "answer": answer, "permutations_checked": len(results),
            "optimal_orders_count": len(optimal_orders), "available_ratio_greedy": evaluate(greedy),
            "dynamic_program_minimum": total}

if __name__ == "__main__":
    print(json.dumps(solve(), sort_keys=True))
