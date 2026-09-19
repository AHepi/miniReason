"""
What this file does
-------------------
Runs the experiment frozen in "11 Test design - do kinds emerge from selection".

A small world: a line of cells with one or two moving things. A thinker sees only
which cells are occupied (no identity, no velocity) and must predict the true
occupancy at the next step. Every possible predictor architecture from a small
fixed grammar is evaluated on several histories of exposure. We then ask which
architectures each history selects, whether the selected ones contain components
that respond to changes the way a thing does (a "thing-kind"), and whether a
blind mutation-selection search lands on the same architectures.

Everything is exact: every configuration, every change, every architecture is
enumerated. No random sampling in the primary result. The evolutionary secondary
uses fixed seeds.

Run:  python3 kinds_from_selection.py  [output_directory]
"""

import itertools
import json
import os
import random
import sys
import hashlib
from collections import defaultdict

# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------

RUN_LENGTH = 9          # time points 0..9
CHANGE_STEP = 3         # the change is applied before recording time point 3
FIRST_SCORED_STEP = 2   # predictions for time points 2..9 are scored
OCCLUSION_WIDTH = 3


def step_kinematics(cell, velocity, num_cells):
    """Move one step with reflecting walls."""
    new_cell = cell + velocity
    if new_cell < 0 or new_cell >= num_cells:
        velocity = -velocity
        new_cell = cell + velocity
    return new_cell, velocity


def occupancy_bits(things, num_cells):
    bits = 0
    for cell, _ in things:
        bits |= 1 << cell
    return bits


def enumerate_configurations(num_cells, num_things):
    """Unordered multisets of (cell, velocity) per thing."""
    states = [(c, v) for c in range(num_cells) for v in (-1, 0, 1)]
    return [list(combo) for combo in itertools.combinations_with_replacement(states, num_things)]


def enumerate_changes(num_cells, num_things):
    changes = [("identity",)]
    for i in range(num_things):
        for c in range(num_cells):
            changes.append(("displace", i, c))
    for i in range(num_things):
        for v in (-1, 0, 1):
            changes.append(("set_velocity", i, v))
    for lo in range(0, num_cells - OCCLUSION_WIDTH + 1):
        changes.append(("occlude", lo, lo + OCCLUSION_WIDTH - 1))
    if num_things == 2:
        changes.append(("swap",))
    return changes


def change_type(change):
    return change[0]


def apply_change_to_world(things, change):
    """Returns (new_things, occluded_cells)."""
    things = [list(t) for t in things]
    occluded = set()
    kind = change[0]
    if kind == "identity":
        pass
    elif kind == "displace":
        _, i, c = change
        things[i][0] = c
    elif kind == "set_velocity":
        _, i, v = change
        things[i][1] = v
    elif kind == "occlude":
        _, lo, hi = change
        occluded = set(range(lo, hi + 1))
    elif kind == "swap":
        things[0], things[1] = things[1], things[0]
    return [tuple(t) for t in things], occluded


def generate_sequence(configuration, change, num_cells):
    """
    Returns a list over time points 0..RUN_LENGTH of dicts:
      sensory: occupancy bits with occluded cells zeroed
      true:    true occupancy bits
      things:  list of (cell, velocity) per thing (identity-indexed)
    """
    things = [tuple(t) for t in configuration]
    occluded = set()
    out = []
    for t in range(RUN_LENGTH + 1):
        if t == CHANGE_STEP:
            things, occluded = apply_change_to_world(things, change)
        true_bits = occupancy_bits(things, num_cells)
        sensory_bits = true_bits
        for c in occluded:
            sensory_bits &= ~(1 << c)
        out.append({"sensory": sensory_bits, "true": true_bits, "things": list(things)})
        things = [step_kinematics(c, v, num_cells) for c, v in things]
    return out


def split_history(history, num_cells, num_things):
    """Exposure half = even-index configurations; evaluation half = odd-index."""
    confs = enumerate_configurations(num_cells, num_things)
    even = {tuple(c) for i, c in enumerate(confs) if i % 2 == 0}
    exposure = [s for s in history if tuple(s[0]) in even]
    evaluation = [s for s in history if tuple(s[0]) not in even]
    return exposure, evaluation


def build_history(num_cells, num_things, change_types_included):
    """A history is a list of (configuration, change, sequence)."""
    seqs = []
    for configuration in enumerate_configurations(num_cells, num_things):
        for change in enumerate_changes(num_cells, num_things):
            if change_type(change) in change_types_included:
                seqs.append((configuration, change, generate_sequence(configuration, change, num_cells)))
    return seqs


# ---------------------------------------------------------------------------
# Architectures (the latent machinery)
# ---------------------------------------------------------------------------

READ_IN_RULES = [("rebind", None, None, None)] + [
    ("persist", tau, radius, jump_keeps)
    for tau in (0, 2, 5, "inf") for radius in (2, 5) for jump_keeps in (False, True)
]


def enumerate_architectures():
    """
    Returns a list of distinct architectures as dicts:
      use_lookup, k, num_slots, rule
    Redundant combinations (k when lookup off, rule when no slots) are collapsed.
    """
    archs = []
    seen = set()
    for use_lookup in (False, True):
        for k in (1, 2, 3):
            for num_slots in (0, 1, 2, 3):
                for rule in READ_IN_RULES:
                    key = (use_lookup, k if use_lookup else None, num_slots, rule if num_slots else None)
                    if key in seen:
                        continue
                    seen.add(key)
                    archs.append({"use_lookup": use_lookup, "k": k if use_lookup else None,
                                  "num_slots": num_slots, "rule": rule if num_slots else None})
    return archs


def architecture_name(a):
    parts = []
    if a["use_lookup"]:
        parts.append(f"lookup(k={a['k']})")
    if a["num_slots"]:
        r = a["rule"]
        rname = "rebind" if r[0] == "rebind" else f"persist(tau={r[1]},r={r[2]},jump_keeps_v={'T' if r[3] else 'F'})"
        parts.append(f"slots={a['num_slots']}:{rname}")
    return " + ".join(parts) if parts else "nothing"


def occupied_cells(bits, num_cells):
    return [c for c in range(num_cells) if bits >> c & 1]


def clip_sign(x):
    return (x > 0) - (x < 0)


def infer_velocity(previous_field, cell, num_cells):
    """Guess a velocity for a newly seen occupant of `cell` from the previous field."""
    if previous_field is None:
        return 0
    if cell - 1 >= 0 and previous_field >> (cell - 1) & 1:
        return 1
    if cell + 1 < num_cells and previous_field >> (cell + 1) & 1:
        return -1
    return 0


class Predictor:
    """One architecture, instantiated with mutable state for a run."""

    def __init__(self, architecture, num_cells, lookup_table=None):
        self.a = architecture
        self.num_cells = num_cells
        self.table = lookup_table if lookup_table is not None else {}
        self.reset()

    def reset(self):
        self.buffer = []
        self.previous_field = None
        # slot: dict(cell, vel, count, prev_cell) or None
        self.slots = [None] * (self.a["num_slots"] or 0)

    # -- slot machinery ----------------------------------------------------

    def advance_slots(self):
        for s in self.slots:
            if s is None:
                continue
            s["prev_cell"] = s["cell"]
            s["cell"], s["vel"] = step_kinematics(s["cell"], s["vel"], self.num_cells)

    def reconcile_slots(self, field):
        rule = self.a["rule"]
        if rule is None:
            return
        if rule[0] == "rebind":
            self.slots = [None] * len(self.slots)
            free = 0
            for c in occupied_cells(field, self.num_cells):
                if free >= len(self.slots):
                    break
                vel = infer_velocity(self.previous_field, c, self.num_cells)
                self.slots[free] = {"cell": c, "vel": vel, "count": 0, "prev_cell": c}
                free += 1
            return

        _, tau, radius, jump_keeps = rule
        confirmed = [s is not None and (field >> s["cell"] & 1) == 1 for s in self.slots]
        for i, s in enumerate(self.slots):
            if s is not None and not confirmed[i]:
                s["count"] += 1
        matched = {s["cell"] for i, s in enumerate(self.slots) if s is not None and confirmed[i]}
        for c in occupied_cells(field, self.num_cells):
            if c in matched:
                continue
            candidates = [(abs(s["cell"] - c), i) for i, s in enumerate(self.slots)
                          if s is not None and not confirmed[i] and abs(s["cell"] - c) <= radius]
            if candidates:
                _, i = min(candidates)
                s = self.slots[i]
                if not (jump_keeps and abs(c - s["prev_cell"]) > 1):
                    s["vel"] = clip_sign(c - s["prev_cell"])
                s["cell"] = c
                s["count"] = 0
                confirmed[i] = True
                matched.add(c)
                continue
            for i, s in enumerate(self.slots):
                if s is None:
                    vel = infer_velocity(self.previous_field, c, self.num_cells)
                    self.slots[i] = {"cell": c, "vel": vel, "count": 0, "prev_cell": c}
                    confirmed[i] = True
                    matched.add(c)
                    break
        if tau != "inf":
            for i, s in enumerate(self.slots):
                if s is not None and s["count"] > tau:
                    self.slots[i] = None

    # -- observe / predict --------------------------------------------------

    def observe(self, field):
        self.advance_slots()
        self.reconcile_slots(field)
        self.previous_field = field
        if self.a["use_lookup"]:
            self.buffer.append(field)
            if len(self.buffer) > self.a["k"]:
                self.buffer.pop(0)

    def lookup_key(self):
        if not self.a["use_lookup"] or not self.buffer:
            return None
        return tuple(self.buffer)  # longest available prefix, at most k fields

    def predict(self):
        bits = 0
        for s in self.slots:
            if s is None:
                continue
            nc, _ = step_kinematics(s["cell"], s["vel"], self.num_cells)
            bits |= 1 << nc
        key = self.lookup_key()
        if key is not None:
            bits |= self.table.get(key, 0)
        return bits

    def slot_states(self):
        return [None if s is None else (s["cell"], s["vel"]) for s in self.slots]


# ---------------------------------------------------------------------------
# Exposure (lookup learning) and evaluation
# ---------------------------------------------------------------------------

def expose_lookup(architecture, history, num_cells):
    """One pass over the history filling the lookup table. Last-writer-wins."""
    if not architecture["use_lookup"]:
        return {}
    table = {}
    p = Predictor(architecture, num_cells, table)
    for _, _, seq in history:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            key = p.lookup_key()
            if key is not None:
                table[key] = seq[t + 1]["true"]
    return table


def sensory_ceiling(history):
    """Best possible prediction from sensation alone on this history: a full-prefix
    memoriser that predicts the most common continuation of each prefix. This is
    the best deterministic predictor from sensation on this history, and an upper
    bound for every architecture."""
    counts = {}
    for _, _, seq in history:
        for t in range(RUN_LENGTH):
            key = tuple(s["sensory"] for s in seq[:t + 1])
            counts.setdefault(key, defaultdict(int))[seq[t + 1]["true"]] += 1
    best = {key: max(c.items(), key=lambda kv: (kv[1], -kv[0]))[0] for key, c in counts.items()}
    correct = total = 0
    by_type = defaultdict(lambda: [0, 0])
    for _, change, seq in history:
        ct = change_type(change)
        for t in range(RUN_LENGTH):
            if t + 1 < FIRST_SCORED_STEP:
                continue
            key = tuple(s["sensory"] for s in seq[:t + 1])
            ok = best[key] == seq[t + 1]["true"]
            correct += ok
            total += 1
            by_type[ct][0] += ok
            by_type[ct][1] += 1
    return correct / total, {k: v[0] / v[1] for k, v in by_type.items()}


def evaluate(architecture, table, history, num_cells):
    """Returns (fitness, per_change_type_fitness)."""
    p = Predictor(architecture, num_cells, table)
    correct = 0
    total = 0
    by_type = defaultdict(lambda: [0, 0])
    for _, change, seq in history:
        p.reset()
        ct = change_type(change)
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= FIRST_SCORED_STEP:
                ok = p.predict() == seq[t + 1]["true"]
                correct += ok
                total += 1
                by_type[ct][0] += ok
                by_type[ct][1] += 1
    return correct / total, {k: v[0] / v[1] for k, v in by_type.items()}


# ---------------------------------------------------------------------------
# M3: thing-signature under translated edits (2-thing world)
# ---------------------------------------------------------------------------

def apply_translated_change(predictor, change, binding):
    """binding: dict slot_index -> thing_index. Returns new binding."""
    kind = change[0]
    inverse = {thing: slot for slot, thing in binding.items()}
    if kind == "displace":
        _, i, c = change
        s = predictor.slots[inverse[i]]
        s["cell"] = c
        s["prev_cell"] = c
    elif kind == "set_velocity":
        _, i, v = change
        predictor.slots[inverse[i]]["vel"] = v
    elif kind == "swap":
        binding = {slot: 1 - thing for slot, thing in binding.items()}
    return binding


def thing_signature(architecture, num_cells, configurations, changes):
    """
    For each (configuration, change): run unchanged to step CHANGE_STEP-1, match
    slots to things, apply translated change, run on with the changed sensory
    stream, check every bound slot tracks its thing's (cell, velocity) exactly.
    Returns fraction passing overall and by change type, plus count of pairs
    where no binding could be established (predictor was not tracking).
    """
    if not architecture["num_slots"]:
        return None
    p = Predictor(architecture, num_cells, {})
    passed = 0
    total = 0
    by_type = defaultdict(lambda: [0, 0])
    unbound = 0
    for configuration in configurations:
        unchanged = generate_sequence(configuration, ("identity",), num_cells)
        for change in changes:
            total += 1
            ct = change_type(change)
            by_type[ct][1] += 1
            changed = generate_sequence(configuration, change, num_cells)
            p.reset()
            for t in range(CHANGE_STEP):
                p.observe(unchanged[t]["sensory"])
            # establish binding from slot states vs thing states at step CHANGE_STEP-1
            things = unchanged[CHANGE_STEP - 1]["things"]
            binding = {}
            used = set()
            ok = True
            for si, st in enumerate(p.slot_states()):
                if st is None:
                    continue
                found = None
                for ti, th in enumerate(things):
                    if ti not in used and tuple(th) == st:
                        found = ti
                        break
                if found is None:
                    ok = False
                    break
                binding[si] = found
                used.add(found)
            if not ok or len(binding) != len(things):
                unbound += 1
                continue
            # step to CHANGE_STEP: advance, apply translated change, reconcile
            p.advance_slots()
            binding = apply_translated_change(p, change, binding)
            p.reconcile_slots(changed[CHANGE_STEP]["sensory"])
            p.previous_field = changed[CHANGE_STEP]["sensory"]
            tracking = True
            for t in range(CHANGE_STEP, RUN_LENGTH + 1):
                if t > CHANGE_STEP:
                    p.observe(changed[t]["sensory"])
                states = p.slot_states()
                for si, ti in binding.items():
                    if states[si] is None or states[si] != tuple(changed[t]["things"][ti]):
                        tracking = False
                        break
                if not tracking:
                    break
            if tracking:
                passed += 1
                by_type[ct][0] += 1
    return {"fraction": passed / total, "by_type": {k: v[0] / v[1] for k, v in by_type.items()},
            "unbound_pairs": unbound, "total_pairs": total}


# ---------------------------------------------------------------------------
# Evolutionary secondary
# ---------------------------------------------------------------------------

def mutate(architecture, rng):
    a = dict(architecture)
    choice = rng.choice(["lookup", "k", "slots", "rule"])
    if choice == "lookup":
        a["use_lookup"] = not a["use_lookup"]
        a["k"] = rng.choice([1, 2, 3]) if a["use_lookup"] else None
    elif choice == "k" and a["use_lookup"]:
        a["k"] = rng.choice([1, 2, 3])
    elif choice == "slots":
        a["num_slots"] = max(0, min(3, a["num_slots"] + rng.choice([-1, 1])))
        a["rule"] = (a["rule"] or rng.choice(READ_IN_RULES)) if a["num_slots"] else None
    elif choice == "rule" and a["num_slots"]:
        a["rule"] = rng.choice(READ_IN_RULES)
    return a


def arch_key(a):
    return (a["use_lookup"], a["k"], a["num_slots"], a["rule"])


def evolve(history, num_cells, num_things, seed, fitness_cache, population_size=32, elite=4, generations=40):
    rng = random.Random(seed)
    all_archs = enumerate_architectures()
    population = [dict(rng.choice(all_archs)) for _ in range(population_size)]
    exposure, evaluation = split_history(history, num_cells, num_things)

    def fitness(a):
        key = arch_key(a)
        if key not in fitness_cache:
            table = expose_lookup(a, exposure, num_cells)
            fitness_cache[key] = evaluate(a, table, evaluation, num_cells)[0]
        return fitness_cache[key]

    trajectory = []
    for gen in range(generations):
        scored = sorted(population, key=fitness, reverse=True)
        best = scored[0]
        trajectory.append({"generation": gen, "best": architecture_name(best), "best_fitness": fitness(best)})
        elites = scored[:elite]
        children = list(elites)
        while len(children) < population_size:
            parent = rng.choice(elites)
            children.append(mutate(parent, rng))
        population = children
    final = sorted(population, key=fitness, reverse=True)
    counts = defaultdict(int)
    for a in final:
        counts[architecture_name(a)] += 1
    return {"seed": seed, "final_best": architecture_name(final[0]), "final_best_fitness": fitness(final[0]),
            "final_population": dict(counts), "trajectory_end": trajectory[-1]}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def best_of(archs, history, num_cells, num_things):
    exposure, evaluation = split_history(history, num_cells, num_things)
    best = None
    for a in archs:
        table = expose_lookup(a, exposure, num_cells)
        f, _ = evaluate(a, table, evaluation, num_cells)
        if best is None or f > best[0]:
            best = (f, architecture_name(a))
    return {"fitness": best[0], "architecture": best[1]}


def persistence_of(a):
    if not a["num_slots"]:
        return None
    r = a["rule"]
    return "rebind" if r[0] == "rebind" else f"tau={r[1]}"


def run_controls():
    """Section 5 / section 8 step 2 of the design (as amended).
    Neutrality: on H_neutral, the best architecture for each persistence value
                (rebind, tau=0, 2, 5, inf) all within 0.01 of each other.
    Adequacy:   on H_full, best slot-only > best lookup-only and >= 0.95 * ceiling.
    Also reported: lookup-only vs slot-only on both (object-model axis)."""
    archs = enumerate_architectures()
    lookup_only = [a for a in archs if a["use_lookup"] and not a["num_slots"]]
    slot_only = [a for a in archs if a["num_slots"] and not a["use_lookup"]]
    h_neutral = build_history(6, 1, {"identity", "displace", "set_velocity"})
    h_full = build_history(6, 2, {"identity", "displace", "set_velocity", "occlude", "swap"})
    out = {}
    for hname, h, nt in (("H_neutral", h_neutral, 1), ("H_full", h_full, 2)):
        _, evaluation = split_history(h, 6, nt)
        out[f"ceiling_{hname}_evaluation_half"] = sensory_ceiling(evaluation)[0]
        per = {}
        for pv in ("rebind", "tau=0", "tau=2", "tau=5", "tau=inf"):
            per[pv] = best_of([a for a in slot_only if persistence_of(a) == pv], h, 6, nt)
        out[f"{hname}_best_per_persistence"] = per
        out[f"{hname}_best_lookup_only"] = best_of(lookup_only, h, 6, nt)
        out[f"{hname}_best_slot_only"] = best_of(slot_only, h, 6, nt)
    tau_vals = [v["fitness"] for pv, v in out["H_neutral_best_per_persistence"].items() if pv != "rebind"]
    out["neutrality_check_passes"] = (max(tau_vals) - min(tau_vals)) <= 0.01
    f_l, f_s = out["H_full_best_lookup_only"]["fitness"], out["H_full_best_slot_only"]["fitness"]
    out["adequacy_check_passes"] = f_s > f_l
    out["H_full_best_slot_fraction_of_ceiling"] = f_s / out["ceiling_H_full_evaluation_half"]
    return out


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    results = {"design": "11 Test design - do kinds emerge from selection", "code_sha256": sha256_of_file(__file__)}

    histories = {
        "H_neutral": (6, 1, {"identity", "displace", "set_velocity"}),
        "H_passive": (6, 2, {"identity"}),
        "H_kinematic": (6, 2, {"identity", "displace", "set_velocity"}),
        "H_full": (6, 2, {"identity", "displace", "set_velocity", "occlude", "swap"}),
    }
    full_contract = {1: build_history(6, 1, {"identity", "displace", "set_velocity", "occlude"}),
                     2: build_history(6, 2, {"identity", "displace", "set_velocity", "occlude", "swap"})}
    full_eval = {n: split_history(full_contract[n], 6, n)[1] for n in (1, 2)}
    built = {name: build_history(*spec) for name, spec in histories.items()}
    split = {name: split_history(h, histories[name][0], histories[name][1]) for name, h in built.items()}
    results["history_sizes"] = {name: {"exposure": len(split[name][0]), "evaluation": len(split[name][1])}
                                for name in built}
    results["protocol"] = "exposure on even-index configurations; every fitness is on the odd-index half"
    results["ceilings"] = {name: dict(zip(("fitness", "by_type"), sensory_ceiling(split[name][1])))
                           for name in built}
    for n in (1, 2):
        results["ceilings"][f"full_contract_{n}_thing"] = dict(zip(("fitness", "by_type"), sensory_ceiling(full_eval[n])))

    archs = enumerate_architectures()
    results["num_architectures"] = len(archs)

    # M1, M2, M4
    table_rows = []
    for a in archs:
        row = {"architecture": architecture_name(a), "M1": {}, "M2": {}}
        for hname, (num_cells, num_things, _) in histories.items():
            exposure, evaluation = split[hname]
            table = expose_lookup(a, exposure, num_cells)
            m1, _ = evaluate(a, table, evaluation, num_cells)
            m2, m2_by_type = evaluate(a, table, full_eval[num_things], num_cells)
            row["M1"][hname] = m1
            row["M2"][hname] = {"fitness": m2, "by_type": m2_by_type}
        table_rows.append(row)
    results["table"] = table_rows

    # selected sets (fitness-maximal per history)
    selected = {}
    for hname in histories:
        best = max(r["M1"][hname] for r in table_rows)
        selected[hname] = {"max_fitness": best,
                           "architectures": [r["architecture"] for r in table_rows if r["M1"][hname] == best]}
    results["selected"] = selected

    # M3
    confs = enumerate_configurations(6, 2)
    chgs = enumerate_changes(6, 2)
    m3 = {}
    for a in archs:
        if a["use_lookup"] or not a["num_slots"]:
            continue
        m3[architecture_name(a)] = thing_signature(a, 6, confs, chgs)
    results["M3"] = m3

    # evolutionary secondary
    evo = {}
    for hname in ("H_neutral", "H_passive", "H_full"):
        num_cells, num_things = histories[hname][0], histories[hname][1]
        cache = {}
        evo[hname] = [evolve(built[hname], num_cells, num_things, seed, cache) for seed in range(6)]
    results["evolution"] = evo

    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=1, default=str)
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--controls":
        print(json.dumps(run_controls(), indent=1, default=str))
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        r = main(out)
        print(json.dumps({"selected": r["selected"], "history_sizes": r["history_sizes"],
                          "num_architectures": r["num_architectures"]}, indent=1, default=str))
