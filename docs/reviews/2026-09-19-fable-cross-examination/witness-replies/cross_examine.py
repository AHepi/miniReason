"""
What this file does
-------------------
Adversarial cross-examination harness. Sends a document plus an attack prompt to
an OpenAI-compatible chat endpoint, several times, and saves every raw reply.
The replies are witness statements, not verdicts: adjudication happens after,
by hand, in the findings file. Keys come from the environment only and are never
written to any output.

Usage: python3 cross_examine.py <battery.json> <out_dir> [--samples N] [--workers N]
"""
import json, os, sys, time, hashlib, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

ENDPOINT = os.environ.get("XEXAM_ENDPOINT", "https://api.atria-asi.ai/v1/chat/completions")
KEY = os.environ.get("XEXAM_KEY", "")
MODEL = os.environ.get("XEXAM_MODEL", "")

SYSTEM = ("You are a hostile, meticulous referee for a philosophy-of-science and computational "
          "experiment submission. Your job is to find what is WRONG: hidden assumptions, circularity, "
          "invalid inferences, confounds, bugs, moved goalposts, and overclaims. Quote the exact passage "
          "you are attacking. Number every finding. For each finding state: (1) the claim attacked, "
          "(2) why it fails, (3) how serious it is (fatal / serious / minor / cosmetic), (4) what would "
          "fix it. Do not praise. Do not summarise the document. If you genuinely find nothing wrong "
          "with a section, say so in one line and move on. Be specific enough that the author can "
          "check each finding against the text. Keep any private reasoning brief; every finding must appear in your "
          "final answer, not only in your thinking.")


def call(messages, temperature, max_tokens=int(os.environ.get("XEXAM_MAX_TOKENS", "24000")), retries=4):
    payload = {"model": MODEL, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    stream = os.environ.get("XEXAM_STREAM") == "1"  # keep the connection alive past a fixed idle cut
    if stream:
        payload["stream"] = True
        payload["stream_options"] = {"include_usage": True}
    data = json.dumps(payload).encode()
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(ENDPOINT, data=data, method="POST",
                                     headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=int(os.environ.get("XEXAM_TIMEOUT", "1800"))) as r:
                if stream:
                    content, reasoning, usage, finish = [], [], {}, None
                    for raw in r:
                        line = raw.decode().strip()
                        if not line.startswith("data:"):
                            continue
                        line = line[5:].strip()
                        if line == "[DONE]":
                            break
                        chunk = json.loads(line)
                        if chunk.get("usage"):
                            usage = chunk["usage"]
                        for ch in chunk.get("choices", []):
                            d = ch.get("delta", {})
                            if d.get("content"):
                                content.append(d["content"])
                            if d.get("reasoning_content"):
                                reasoning.append(d["reasoning_content"])
                            if ch.get("finish_reason"):
                                finish = ch["finish_reason"]
                    usage["finish_reason"] = finish
                    if finish is None:  # the stream ended without a finish marker: the connection was cut
                        raise ConnectionError(f"stream cut after {sum(map(len, reasoning))} reasoning chars and {sum(map(len, content))} content chars")
                    return {"content": "".join(content), "reasoning": "".join(reasoning)}, usage, None
                body = json.loads(r.read().decode())
                msg = body["choices"][0]["message"]
                content = msg.get("content") or ""
                reasoning = msg.get("reasoning_content") or ""
                usage = body.get("usage", {})
                usage["finish_reason"] = body["choices"][0].get("finish_reason")
                return {"content": content, "reasoning": reasoning}, usage, None
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode()[:500]}"
            print(f"    retry {attempt + 1}: {last[:120]}", flush=True)
            if e.code in (401, 429, 500, 502, 503, 504):  # 401: Atria reports burst-rate limits as auth errors
                time.sleep(20 * (attempt + 1)); continue
            return None, {}, last
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
            print(f"    retry {attempt + 1}: {last[:120]}", flush=True)
            time.sleep(5 * (attempt + 1))
    return None, {}, last


def run_item(item, sample, docs, out_dir):
    doc_text = "\n\n".join(f"===== DOCUMENT: {d} =====\n{docs[d]}" for d in item["documents"])
    user = f"{item['prompt']}\n\n{doc_text}"
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    t0 = time.time()
    out, usage, err = call(messages, temperature=item.get("temperature", 0.7))
    content = out["content"] if out else None
    rec = {"id": item["id"], "sample": sample, "documents": item["documents"], "prompt": item["prompt"],
           "model": MODEL, "seconds": round(time.time() - t0, 1), "usage": usage, "error": err,
           "reply": content, "reasoning": (out["reasoning"] if out else None),
           "note": (None if (content or err) else "empty content: model exhausted its budget while reasoning")}
    path = os.path.join(out_dir, f"{item['id']}__s{sample}.json")
    with open(path, "w") as f:
        json.dump(rec, f, indent=1)
    return item["id"], sample, err, (len(content) if content else 0)


def main():
    battery = json.load(open(sys.argv[1]))
    out_dir = sys.argv[2]
    samples = int(sys.argv[sys.argv.index("--samples") + 1]) if "--samples" in sys.argv else 2
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    os.makedirs(out_dir, exist_ok=True)
    docs = {name: open(path).read() for name, path in battery["documents"].items()}
    only = os.environ.get("XEXAM_ONLY")  # comma-separated "id:sample" pairs for reruns
    if only:
        wanted = {tuple(x.split(":")) for x in only.split(",")}
        jobs = [(item, int(s)) for item in battery["items"] for (iid, s) in wanted if item["id"] == iid]
    else:
        jobs = [(item, s) for item in battery["items"] for s in range(samples)]
    print(f"{len(jobs)} calls to {MODEL} at {ENDPOINT}", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(run_item, item, s, docs, out_dir) for item, s in jobs]
        for fut in as_completed(futs):
            iid, s, err, n = fut.result()
            print(f"  {iid} s{s}: {'ERROR ' + err if err else f'{n} chars'}", flush=True)


if __name__ == "__main__":
    main()
