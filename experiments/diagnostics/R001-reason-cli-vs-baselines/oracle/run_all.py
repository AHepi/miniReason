"""Execute the eight sealed oracles and compare their exact answer objects."""
from pathlib import Path
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent

def read_text(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return stream.read()

def expected(path):
    lines = read_text(path).splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == "```json"]
    if len(starts) != 1:
        raise ValueError("Expected exactly one sealed JSON block: " + path.name)
    start = starts[0] + 1
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == "```")
    return json.loads("\n".join(lines[start:end]))

def main():
    env = dict(os.environ)
    for key in ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY"):
        env.pop(key, None)
    env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    for number in range(1, 9):
        ident = "P" + str(number).zfill(2)
        sealed = expected(STUDY / "answers" / (ident + ".md"))
        result = subprocess.run([sys.executable, "-B", str(HERE / (ident + ".py"))],
            cwd=STUDY, env=env, capture_output=True, text=True, encoding="utf-8",
            timeout=120, check=False)
        if result.returncode:
            print(ident + " ORACLE_FAILED")
            print(result.stderr)
            return 1
        observed = json.loads(result.stdout)
        if observed.get("problem_id") != ident or sealed.get("problem_id") != ident:
            raise ValueError(ident + " identity mismatch")
        if observed["answer"] != sealed["answer"]:
            raise ValueError(ident + " oracle differs from sealed answer")
        target = HERE / (ident + ".output.json")
        output = json.dumps(observed, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if target.exists():
            if read_text(target) != output:
                raise ValueError(ident + " prior oracle output differs; preserve and investigate")
        else:
            with target.open("w", encoding="utf-8", newline="") as stream:
                stream.write(output)
        print(ident + " PASS " + json.dumps(observed["answer"], sort_keys=True))
    print("ALL 8 ORACLES AGREE WITH SEALED ANSWERS; no participant execution")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
