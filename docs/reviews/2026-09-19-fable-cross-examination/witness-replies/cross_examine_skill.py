"""
What this file does
-------------------
A variant of cross_examine.py that gives the witness a METHOD SKILL instead of the
plain referee instruction. The skill's SKILL.md and every file in its references/
folder are pasted verbatim into the system prompt, followed by a short framing that
tells the witness to run the skill's own procedure on the document and to report in
the skill's own format. The item prompts (the attack questions) are the same as in
the plain run, so the only thing that changes between the two runs is the method.

Usage: XEXAM_SKILL_DIR=<dir containing SKILL.md> XEXAM_SKILL_FRAME=<framing text file>
       python3 cross_examine_skill.py <battery.json> <out_dir> [--samples N] [--workers N]
Every other setting (endpoint, model, key, cap, streaming, timeout) is read from the
same environment variables as cross_examine.py. Keys are never written to any output.
"""
import os, sys, glob
import cross_examine as base

skill_dir = os.environ["XEXAM_SKILL_DIR"]
frame = open(os.environ["XEXAM_SKILL_FRAME"]).read()
parts = [open(os.path.join(skill_dir, "SKILL.md")).read()]
for path in sorted(glob.glob(os.path.join(skill_dir, "references", "*.md"))):
    parts.append(f"\n\n===== references/{os.path.basename(path)} =====\n" + open(path).read())
base.SYSTEM = frame + "\n\n===== SKILL.md =====\n" + "".join(parts)
base.SKILL_NAME = os.path.basename(os.path.normpath(skill_dir))

_run_item = base.run_item
def run_item(item, sample, docs, out_dir):
    iid, s, err, n = _run_item(item, sample, docs, out_dir)
    import json
    path = os.path.join(out_dir, f"{item['id']}__s{sample}.json")
    rec = json.load(open(path))
    rec["method_skill"] = base.SKILL_NAME
    rec["system_prompt_chars"] = len(base.SYSTEM)
    json.dump(rec, open(path, "w"), indent=1)
    return iid, s, err, n
base.run_item = run_item

if __name__ == "__main__":
    print(f"system prompt: {len(base.SYSTEM)} chars from skill '{base.SKILL_NAME}'", flush=True)
    base.main()
