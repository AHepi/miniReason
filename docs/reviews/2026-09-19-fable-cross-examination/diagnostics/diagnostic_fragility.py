# What this file does: checks whether experiment 1's winner on H_full (a two-slot
# tracker that never forgets, tau=inf) really beats the tracker that forgets after
# five steps (tau=5), or whether the 0.003 gap is noise from which configurations
# happened to land in the evaluation half. It scores both trackers per configuration
# on the evaluation half of H_full, then (a) counts configurations where each wins,
# (b) draws 2,000 bootstrap resamples of configurations and reports how often the
# tau=inf tracker still wins, and (c) repeats selection under the opposite split
# (odd-index configurations as evaluation). The frozen code is imported unchanged.
import json, random
from collections import defaultdict
import kinds_from_selection as k

h_full = k.build_history(6, 2, {"identity", "displace", "set_velocity", "occlude", "swap"})
exposure, evaluation = k.split_history(h_full, 6, 2)

def find(name):
    for a in k.enumerate_architectures():
        if k.architecture_name(a) == name:
            return a
    raise KeyError(name)

A_inf = find("slots=2:persist(tau=inf,r=5,jump_keeps_v=F)")
A_5 = find("slots=2:persist(tau=5,r=5,jump_keeps_v=F)")

def per_configuration(architecture, history):
    p = k.Predictor(architecture, 6, None)
    out = defaultdict(lambda: [0, 0])
    for configuration, change, seq in history:
        p.reset()
        for t in range(k.RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= k.FIRST_SCORED_STEP:
                out[json.dumps(configuration)][0] += (p.predict() == seq[t + 1]["true"])
                out[json.dumps(configuration)][1] += 1
    return out

res = {}
for split_name, hist in (("evaluation_half_as_frozen", evaluation), ("exposure_half_as_alternative_split", exposure)):
    s_inf, s_5 = per_configuration(A_inf, hist), per_configuration(A_5, hist)
    configs = sorted(s_inf)
    f_inf = sum(v[0] for v in s_inf.values()) / sum(v[1] for v in s_inf.values())
    f_5 = sum(v[0] for v in s_5.values()) / sum(v[1] for v in s_5.values())
    wins_inf = sum(1 for c in configs if s_inf[c][0] > s_5[c][0])
    wins_5 = sum(1 for c in configs if s_inf[c][0] < s_5[c][0])
    ties = len(configs) - wins_inf - wins_5
    rng = random.Random(0)
    B = 2000; inf_ahead = 0
    for _ in range(B):
        sample = [configs[rng.randrange(len(configs))] for _ in configs]
        ci = sum(s_inf[c][0] for c in sample); c5 = sum(s_5[c][0] for c in sample)
        inf_ahead += (ci > c5)
    res[split_name] = {"configurations": len(configs), "fitness_tau_inf": round(f_inf, 4), "fitness_tau_5": round(f_5, 4),
                       "gap": round(f_inf - f_5, 4), "configs_where_inf_better": wins_inf,
                       "configs_where_5_better": wins_5, "configs_tied": ties,
                       "bootstrap_fraction_inf_ahead": inf_ahead / B}
json.dump(res, open("results_out_fragility.json", "w"), indent=1)
print(json.dumps(res, indent=1))
