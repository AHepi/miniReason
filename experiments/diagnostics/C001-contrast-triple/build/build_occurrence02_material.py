"""Build C001 occurrence-02's material from the PUBLISHED occurrence-01 material.

Provenance, not authorship. This script reads
`experiments/diagnostics/C001-contrast-triple/material.json` (sha256
94edfe612097441c8a5957c41a8a1140833b89bd155bd9794b60a1bfb8979975, the bytes REC-20260914-U
published and occurrence-01's plan pins as `material_sha256`) and changes exactly nine
things. Everything else -- every arm block, every case body, every recoded unit, every
prompt, the reading rule, the node, the seeds, the system message, the public contract,
the envelope, the source pins and the transport pins -- is carried through untouched, so
the two occurrences are the same study at two ceilings on one cell.

    python3 build_occurrence02_material.py <published material.json> <out material.json>

Serialisation is the published file's own: json.dumps(indent=2, sort_keys=True,
ensure_ascii=False) + a trailing newline, verified by round-tripping the input first.
"""
import json
import sys
from pathlib import Path

SOURCE_SHA = '94edfe612097441c8a5957c41a8a1140833b89bd155bd9794b60a1bfb8979975'


def dumps(value: dict) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode('utf-8') + b'\n'


MAX_TOKENS_POLICY = (
    'max_tokens is declared PER ENDPOINT, not once for the study, and the value for each '
    'endpoint is frozen in endpoints[].max_tokens as well as here; `prepare` refuses unless '
    'the two agree and unless every built payload carries its own endpoint\'s value '
    '(CEILING_NOT_APPLIED). In THIS material every endpoint carries 32768, the authorised '
    'maximum. The five Ollama endpoints carried it in occurrence-01 already, on the live '
    'evidence published under REC-20260914-S (F001 occurrence-04, ollama/glm-5.3; '
    'occurrence-05, ollama/kimi-k3: at max_tokens 8192 five nodes returned '
    'INCOMPLETE_GENERATION with finish_reason "length", completion_tokens 8192 and no '
    'content at all, and two further nodes came back PARTIAL). deepseek-flash is raised '
    'from 8192 to 32768 here, BEFORE dispatch, on occurrence-01\'s own terminal records: '
    'its forty coordinates finished COMPLETE 21 / PARTIAL 8 / FAILED 11, and the whole of '
    'that residue is the fcl arm, which is 1 COMPLETE, 8 PARTIAL and 11 FAILED against the '
    'prose arm\'s 20 of 20 at the same ceiling. Every PARTIAL carries finish_reason '
    '"length" at completion_tokens exactly 8192; every FAILED carries INCOMPLETE_GENERATION '
    'with validation_failure_type NO_PUBLIC_CONTENT, no finish_reason and no usage at all; '
    'the nine fcl calls that reported usage spent 5488 to 7890 tokens on reasoning; and the '
    'single fcl COMPLETE finished at 8083, one hundred and nine tokens under the ceiling. '
    'Occurrence-01 gave deepseek-flash 8192 because it "sends no reasoning on the wire, and '
    '8192 was ample for it". Both halves are false of C001 as dispatched: 29 of those 40 '
    'receipts record reasoning_content_present true, and C001\'s briefs are far longer than '
    'the H005 briefs that reason was formed on. That the endpoint ACCEPTS the raised value '
    'is not assumed either: one probe call was sent to deepseek-flash at max_tokens 32768 '
    'with a trivial prompt through this study\'s own transport and came back COMPLETE, '
    'finish_reason "stop", in 1837 ms, its request record carrying max_tokens 32768 and its '
    'usage carrying 81 reasoning tokens of 100. That probe establishes acceptance of the '
    'argument and nothing more: the answer was 100 tokens long, so nothing above 8192 was '
    'exercised, and 32768 is NOT predicted to be sufficient. Raising the ceiling does NOT '
    'manipulate reasoning: temperature, thinking and reasoning_effort are still never sent, '
    'the endpoint default still decides whether and how much it reasons, and the study\'s '
    'own reasoning policy is unchanged. It buys the reply room to exist beside the '
    'reasoning, nothing more. A cell that hits even the raised ceiling is still a PARTIAL or '
    'a refusal, is still marked unresolved and is still compared against nothing '
    '(partial_delivery_rule; FW5:634). One consequence is recorded rather than passed over: '
    'because deepseek-flash now carries what the Ollama endpoints carry, the six endpoints '
    'share a single completion ceiling again, so occurrence-01\'s recorded cost -- that a '
    'deepseek-versus-Ollama difference had one more uncontrolled difference behind it -- '
    'does not apply to this material. NO OCCURRENCE-01 RECORD IS MODIFIED, RELABELLED, '
    'REPAIRED OR SUPERSEDED by this material. Occurrence-01\'s nineteen unusable fcl cells '
    'stay exactly as they are and are still read exactly as PLAN section 6 says; this is a '
    'second ceiling beside the first, which is the rule docs/lessons/operations.md already '
    'records from E001/E002: "new budget conditions require separate freezing rather than '
    'retrospective repair".'
)

TIMEOUT_POLICY_OLD_SENTENCE = 'deepseek-flash keeps the registry\'s own 180 s.'

TIMEOUT_POLICY_NEW_SENTENCE = (
    'In THIS material deepseek-flash carries 600 s as well, and the reason is the raised '
    'completion ceiling. At 8192 its twenty fcl calls in occurrence-01 took 36.0 to 45.7 '
    'seconds of wall clock (median 40.4), an observed generation rate of 179.2 to 227.5 '
    'tokens per second on the fcl arm and 152.6 to 227.5 across all forty of its calls. A '
    'call that spends the whole 32768 ceiling at those same observed rates takes 144 '
    'seconds at the fastest, 183 at the slowest fcl rate and 215 at the slowest rate of the '
    'forty -- two of the three past the 180-second wall clock occurrence-01 gave it. Leaving '
    'the timeout at 180 while quadrupling the ceiling would therefore have planned the same '
    'refusal REC-20260914-T recorded on ollama/glm-5.3 and ollama/kimi-k3: not a ceiling '
    'truncation but a read timeout, TRANSPORT_OR_RESPONSE_ERROR with no finish_reason, no '
    'usage and no content. The extrapolation is arithmetic over published records, not a '
    'prediction about this model, and a call that exceeds even 600 seconds is still a '
    'refusal recorded with its failure code and still compared against nothing.'
)

DISPATCH_SCOPE_REASON = (
    'One cell, dispatched to answer one question occurrence-01 left open: whether the fcl '
    'envelope fits beside deepseek-flash\'s reasoning when the ceiling is not 8192. '
    'Occurrence-01 answered it for the prose arm (20 of 20 COMPLETE) and could not answer '
    'it for the fcl arm (1 of 20). Dispatching the other five endpoints again would re-spend '
    'two hundred calls on cells occurrence-01 already resolved and would answer nothing, and '
    'dispatching the prose arm again would re-spend twenty on an arm that never met the '
    'ceiling. The scope is frozen in plan_id: this occurrence cannot quietly widen it.'
)

ENDPOINT_NOTE = (
    'Registry name in src/minireason/data/endpoints.json. Raised from occurrence-01\'s '
    '8192/180 s to 32768/600 s on that occurrence\'s own terminal records: 19 of its 20 fcl '
    'coordinates were unusable at 8192 (8 PARTIAL at finish_reason "length" with '
    'completion_tokens exactly 8192, 11 FAILED with NO_PUBLIC_CONTENT and no usage), while '
    'the prose arm at the same ceiling was 20 of 20. It DOES send reasoning on the wire, '
    'contrary to occurrence-01\'s note: 29 of its 40 receipts record '
    'reasoning_content_present true, and the nine fcl calls reporting usage spent 5488 to '
    '7890 tokens on reasoning. 32768 was confirmed accepted by one probe call; 600 s is the '
    'transport\'s own validation maximum and is carried because the observed generation rate '
    'puts a full-ceiling call at 144 to 215 seconds. Seed support unverified; the seed is '
    'sent and every record states seed_requested, seed_sent and whether the provider '
    'response echoed a seed.'
)

PARTIAL_DELIVERY_RULE = (
    'A PARTIAL delivery (finish_reason "length" at the endpoint\'s own declared max_tokens '
    'ceiling - 32768 for every endpoint of this material) yields a truncated commitment '
    'surface. Such a cell is marked unresolved in the evidence table and is not compared '
    'against any other case (FW5:634; EXPERIMENT_METHOD operational-failure table). A '
    'delivery that returns no content at all because the ceiling went entirely to reasoning '
    'is a refusal (INCOMPLETE_GENERATION), recorded with its failure code and likewise '
    'compared against nothing. Raising deepseek-flash\'s ceiling from occurrence-01\'s 8192 '
    'makes those outcomes less likely; it does not change how they are read, and it rescues '
    'no cell of occurrence-01, which stands unaltered.'
)


def build(material: dict) -> dict:
    material = json.loads(json.dumps(material))          # never mutate the caller's object
    ceilings = material['ceilings']

    # (1) and (2): the per-endpoint tables, both published places a reader may look.
    ceilings['max_tokens']['deepseek-flash'] = 32768
    ceilings['timeout_seconds']['deepseek-flash'] = 600

    # (3) and (4): the two policies that state why, with their evidence.
    ceilings['max_tokens_policy'] = MAX_TOKENS_POLICY
    old = ceilings['timeout_seconds_policy']
    if TIMEOUT_POLICY_OLD_SENTENCE not in old:
        raise SystemExit('TIMEOUT_POLICY_SENTENCE_NOT_FOUND')
    ceilings['timeout_seconds_policy'] = old.replace(
        TIMEOUT_POLICY_OLD_SENTENCE, TIMEOUT_POLICY_NEW_SENTENCE, 1)

    # (5) and (6): the endpoint entry itself, frozen twice with the tables above.
    entry = next(e for e in material['endpoints'] if e['id'] == 'deepseek-flash')
    entry['max_tokens'] = 32768
    entry['timeout_seconds'] = 600
    entry['note'] = ENDPOINT_NOTE

    # (7): the partial-delivery rule, which named 8192 as deepseek's ceiling.
    material['partial_delivery_rule'] = PARTIAL_DELIVERY_RULE

    # (8): the dispatch scope -- one endpoint, one arm, all four cases, five replicates.
    material['dispatch_scope'] = {
        'endpoints': ['deepseek-flash'],
        'arms': ['fcl'],
        'reason': DISPATCH_SCOPE_REASON,
    }

    # (9): the call count that follows from it. 4 cases x 5 replicates x 1 x 1.
    material['planned_calls'] = 20
    return material


def main(argv: list[str]) -> int:
    source, target = Path(argv[1]), Path(argv[2])
    raw = source.read_bytes()
    import hashlib
    observed = hashlib.sha256(raw).hexdigest()
    if observed != SOURCE_SHA:
        raise SystemExit(f'SOURCE_MATERIAL_NOT_THE_PUBLISHED_BYTES: {observed}')
    published = json.loads(raw)
    if dumps(published) != raw:
        raise SystemExit('SOURCE_MATERIAL_SERIALISATION_UNKNOWN')
    built = build(published)

    # The carry-through is proved, not asserted: every key except the nine is identical.
    changed = {'ceilings', 'endpoints', 'partial_delivery_rule', 'dispatch_scope',
               'planned_calls'}
    for key in set(published) | set(built):
        if key in changed:
            continue
        if published.get(key) != built.get(key):
            raise SystemExit(f'UNDECLARED_MATERIAL_CHANGE: {key}')
    if published['arms'] != built['arms']:
        raise SystemExit('UNDECLARED_MATERIAL_CHANGE: arms')
    others = [e for e in built['endpoints'] if e['id'] != 'deepseek-flash']
    if others != [e for e in published['endpoints'] if e['id'] != 'deepseek-flash']:
        raise SystemExit('UNDECLARED_MATERIAL_CHANGE: endpoints')

    if target.exists():
        raise SystemExit('TARGET_EXISTS')
    target.parent.mkdir(parents=True, exist_ok=True)
    out = dumps(built)
    target.write_bytes(out)
    print(json.dumps({'source_sha256': observed, 'target_sha256': hashlib.sha256(out).hexdigest(),
                      'planned_calls': built['planned_calls'],
                      'deepseek_max_tokens': built['ceilings']['max_tokens']['deepseek-flash'],
                      'deepseek_timeout_seconds':
                          built['ceilings']['timeout_seconds']['deepseek-flash']},
                     sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
