"""Execute the sealed UC1 fallible review as one recorded offline scripted call."""
import argparse
import hashlib
import json
from pathlib import Path

from minireason.reason.adapter import Adapter
from minireason.reason.config import load_endpoint_snapshot


def read_json(path):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError("DUPLICATE_KEY")
            value[key] = item
        return value
    with path.open("r", encoding="utf-8", newline="") as handle:
        return json.load(handle, object_pairs_hook=pairs)


def validate(value, schema, path="$"):
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(path + ": enum")
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(value, dict): raise ValueError(path + ": object")
        if schema.get("additionalProperties") is False and set(value) - set(schema.get("properties", {})):
            raise ValueError(path + ": extra fields")
        for name in schema.get("required", []):
            if name not in value: raise ValueError(path + ": missing " + name)
        for name, item in value.items():
            if name in schema.get("properties", {}): validate(item, schema["properties"][name], path + "." + name)
    elif expected == "array":
        if not isinstance(value, list): raise ValueError(path + ": array")
        for index, item in enumerate(value): validate(item, schema.get("items", {}), path + "[" + str(index) + "]")
    elif expected == "string" and not isinstance(value, str): raise ValueError(path + ": string")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("OUT_MUST_BE_NEW")
    root = Path(__file__).resolve().parent
    template = read_json(root / "review-template.json")
    scripted = read_json(root / "review-positive.scripted.json")
    spec = read_json(root / "shot-spec-positive.json")
    with (root / "blender-blocking-positive.py").open("r", encoding="utf-8", newline="") as handle:
        script = handle.read()
    checker_bytes = (root / "verify_uc1.py").read_bytes()
    checker_identity = "sha256:" + hashlib.sha256(checker_bytes).hexdigest()
    args.out.mkdir(parents=True, exist_ok=False)
    messages = [
        {"role": "system", "content": template["instruction"]},
        {"role": "user", "content": json.dumps({
            "shot_spec_json": spec,
            "blender_script": script,
            "static_verifier_report": {"ok": True, "checker_identity": checker_identity},
        }, ensure_ascii=False, sort_keys=True)},
    ]
    decision = {
        "mode": "offline", "role": template["role"], "thinking": template["thinking"],
        "max_completion_tokens": template["max_completion_tokens"], "schema": template["output_schema"],
        "note": "Scripted fixture only; no provider/model call. Review is same-lineage and fallible."
    }
    with (args.out / "decision.json").open("x", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(decision, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    adapter = Adapter("offline", load_endpoint_snapshot())
    result = adapter.call(
        seat="deepseek-flash",
        messages=messages,
        records_dir=args.out / "provider",
        max_tokens=template["max_completion_tokens"],
        thinking=template["thinking"],
        role=template["role"],
        coordinate={"task": "UC1", "fixture": "fallible-review"},
        scripted=scripted[0],
    )
    parsed = json.loads(result["content"])
    validate(parsed, template["output_schema"])
    with (args.out / "review-result.json").open("x", encoding="utf-8", newline="") as handle:
        handle.write(json.dumps(parsed, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"attempts": 1, "provider_calls": 0, "result": parsed}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
