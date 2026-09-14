"""Two boundary facts:

(a) is the 'prefix intact' rule present in the shipped standard at all, and where;
(b) standard.py names itself "the byte-identical PLAN §8a excerpt and its
    material.json mirror" — data/plan_8a_mirror.json — but nothing in the repo tree
    re-hashes it against experiments/diagnostics/C001-contrast-triple/{PLAN.md,
    material.json}, paths the mirror itself names.
"""
from __future__ import annotations

import hashlib
import json
import os

from _probe_setup import check

from minireason.loop import standard


def flatten_ws(text: str) -> str:
    return " ".join(text.split())


def main() -> None:
    t_plan = standard.PLAN_8A_MIRROR["registers"]["T"]["plan_text"]
    print("raw 'prefix' bytes in T plan_text:", [
        hex(ord(c)) for c in t_plan if c in "\u2010-\u2015"])
    flat = flatten_ws(t_plan)
    needle = "read **with the source artifact prefix intact**"
    print("flattened T plan_text contains the needle:", needle in flat)
    print("flattened T plan_text:", flat)

    # Where does the needle land in the SHIPPED standard body?
    body = json.loads(standard.STANDARD_BODY)
    body_text = json.dumps(body)
    print("needle (whitespace-flattened) anywhere in the rendered body text:",
          needle.replace("*", "") .split()[0] in body_text)

    register_json = json.dumps(body["registers"]["T"], sort_keys=True)
    check("T register in the shipped body carries the prefix-intact rule",
          all(piece in register_json for piece in
              ("prefix", "intact", "source artifact prefix")))

    # (b) the mirror's own declared sources, and whether they exist here.
    source = standard.PLAN_8A_MIRROR["source"]
    print("mirror declares plan_path:", source["plan_path"])
    print("mirror declares material_path:", source["material_path"])
    for field, key in (("plan_path", "plan_sha256"), ("material_path", "material_sha256")):
        print(f"  {field} -> {source[field]}  pinned sha256: {source[key]}")
        check(f"{source[field]} exists in this snapshot",
              os.path.exists(source[field]))

    # grep the whole snapshot for any verification of the two pinned digests.
    found_proof = False
    for root, _dirs, files in os.walk("."):
        for name in files:
            path = os.path.join(root, name)
            if path.startswith("./probe/"):
                continue
            try:
                with open(path, "rb") as handle:
                    data = handle.read()
            except OSError:
                continue
            for digest in (source["plan_sha256"], source["material_sha256"]):
                if digest.encode() in data:
                    found_proof = True
                    print(f"pinned digest found in: {path}")
    check("some file other than the mirror itself re-asserts the pinned digests",
          found_proof)

    # What is hashable here: the mirror file itself.
    mirror_bytes = standard.PLAN_8A_MIRROR_PATH.read_bytes()
    print("sha256(data/plan_8a_mirror.json) =", hashlib.sha256(mirror_bytes).hexdigest())
    print("PLAN.md sha256 the mirror pins  =", source["plan_sha256"])
    print("material.json sha256 it pins    =", source["material_sha256"])
    check("mirror pins are NOT the digest of the mirror file itself",
          hashlib.sha256(mirror_bytes).hexdigest() not in
          (source["plan_sha256"], source["material_sha256"]))


if __name__ == "__main__":
    main()
