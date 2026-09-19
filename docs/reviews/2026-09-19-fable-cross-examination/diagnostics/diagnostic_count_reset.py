# What this file does: a witness said the forgetting counter is never reset when a
# hidden slot re-emerges in place, so the implemented rule is "cumulative unconfirmed
# steps since the last re-bind" rather than "consecutive unconfirmed steps". This
# patches the reconcile step in a subclass (reset the counter whenever a slot is
# confirmed) and re-scores the persistence family on the occlusion history, to see
# whether the ordering of the frozen result depends on that detail.
import json
import kinds_from_selection as k

class PatchedPredictor(k.Predictor):
    def reconcile_slots(self, field):
        super().reconcile_slots(field)
        for s in self.slots:
            if s is not None and (field >> s["cell"] & 1) == 1:
                s["count"] = 0

H_full = k.build_history(6, 2, {"identity", "displace", "set_velocity", "occlude", "swap"})
exposure, evaluation = k.split_history(H_full, 6, 2)
def arch(name):
    for a in k.enumerate_architectures():
        if k.architecture_name(a) == name:
            return a
def score(cls, a, hist):
    p = cls(a, 6, None); correct = total = 0
    for _, change, seq in hist:
        p.reset()
        for t in range(k.RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= k.FIRST_SCORED_STEP:
                correct += (p.predict() == seq[t + 1]["true"]); total += 1
    return round(correct / total, 4)
out = {}
for tau in ("0", "2", "5", "inf"):
    for r in ("2", "5"):
        name = f"slots=2:persist(tau={tau},r={r},jump_keeps_v=F)"
        a = arch(name)
        out[name] = {"frozen": score(k.Predictor, a, evaluation), "count_reset_on_confirm": score(PatchedPredictor, a, evaluation)}
json.dump(out, open("results_out_count_reset.json", "w"), indent=1)
for n, v in out.items(): print(f"{n:45s} frozen {v['frozen']}  patched {v['count_reset_on_confirm']}")
