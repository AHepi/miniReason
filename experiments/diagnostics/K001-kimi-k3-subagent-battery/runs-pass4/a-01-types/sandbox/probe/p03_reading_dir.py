"""Probe: does reading_dir leak a run_id fragment into the directory name?

Run a row_key the slug leaves intact, then check the digest suffix actually
disambiguates collision pairs that fold alike, then check unicode folding.
"""
import sys, hashlib
from pathlib import Path
sys.path.insert(0, "src")

from minireason.loop.types import run_paths

paths = run_paths(Path("/repo"), "run_alpha")

d1 = paths.reading_dir("run_alpha/arm/cycle-1/node#r3")
d2 = paths.reading_dir("run_alpha!arm!cycle-1!node#r3")
print("similar key 1 ->", d1.name)
print("similar key 2 ->", d2.name)
print("distinct:", d1 != d2)
print("plaintext run_id/leak check:", "run_alpha" in d1.name)

# unicode: many distinct keys fold to the same slug; digest must separate
a = paths.reading_dir("café/x")
b = paths.reading_dir("cafexq")  # different key, folded slug 'cafexq' vs 'caf__x'
print("unicode fold:", a.name, "|", b.name, "distinct:", a != b)

# two keys that fold to the SAME slug
k1 = "a/b#c"
k2 = "a_b_c#c".replace("_", "!").replace("#", "?")  # folds to a_b_c_c? force same
k1s = k1; k2s = "a!b!c?c"  # both fold to a_b_c_c
r1 = paths.reading_dir(k1s); r2 = paths.reading_dir(k2s)
folded = [r.name.rsplit("-", 1)[0] for r in (r1, r2)]
print("same-slug pair:", r1.name, "|", r2.name,
      "folded slugs:", folded, "distinct dirs:", r1 != r2)
