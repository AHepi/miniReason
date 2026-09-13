"""Root-authored post-observation finite check; not participant acceptance."""
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, re, sqlite3
from pathlib import Path
ROOT = Path(__file__).resolve().parent
ORACLE = ROOT.parent / 'E028-sql-event-oracle/oracle.json'
KEYS = {'Lrows', 'Rrows', 'LkeyIndex', 'RkeyIndex'}
def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def require(v, code):
    if not v: raise ValueError(code)
def bag(rows): return Counter(json.dumps(r, ensure_ascii=False) for r in rows)
def indexes(rows):
    d = {}
    for r in rows:
        if r[1] is not None: d.setdefault(r[1], []).append(r[0])
    return sorted((k, sorted(ids)) for k, ids in d.items())
def extract(call):
    text = (ROOT / f'responses/{call:04d}.txt').read_bytes().decode('utf-8')
    start = re.search(r'^## Event 1\b', text, re.M) if call in (1,4,6) else None
    if call in (1,4,6): require(start is not None, 'NO_EVENT_HEADING')
    blocks = []
    fence = chr(96) * 3
    for m in re.finditer('^'+fence+r'(?:json)?[ \t]*\r?\n(.*?)^'+fence, text, re.M|re.S):
        if start is not None and m.start() < start.start(): continue
        try: value = json.loads(m[1])
        except json.JSONDecodeError: continue
        blocks.append((value, text[:m.start()].count('\n') + 1))
    states = []
    for i, (v, line) in enumerate(blocks):
        if not isinstance(v, dict) or not KEYS <= v.keys(): continue
        if 'output_bag' in v: out, out_line = v['output_bag'], line
        else:
            require(i+1 < len(blocks), 'NO_OUTPUT_BLOCK')
            out, out_line = blocks[i+1]
            require(isinstance(out, list), 'OUTPUT_NOT_LIST')
        states.append((v,out,line,out_line))
    return states
def compare(call, state, expected, position):
    v,out,line,out_line = state
    checks = {k: bag(v[k]) == bag(expected[k]) for k in ('Lrows','Rrows')}
    checks['output_bag'] = bag(out) == bag(expected['output_bag'])
    for side in ('L','R'):
        checks[side+'keyIndex'] = sorted((k,sorted(ids)) for k,ids in v[side+'keyIndex']) == indexes(expected[side+'rows'])
    return dict(call_id=call, position=position, state_fence_line=line, output_fence_line=out_line, checks=checks, all_equal=all(checks.values()))
def main():
    oracle = read(ORACLE)
    db = sqlite3.connect(':memory:')
    db.executescript('CREATE TABLE L(lid INTEGER PRIMARY KEY,k INTEGER);CREATE TABLE R(rid INTEGER PRIMARY KEY,k INTEGER,v TEXT);')
    db.executemany('INSERT INTO L VALUES (?,?)', oracle['initial']['Lrows'])
    db.executemany('INSERT INTO R VALUES (?,?,?)', oracle['initial']['Rrows'])
    query = 'SELECT ALL L.lid,L.k,R.v FROM L LEFT JOIN R ON L.k=R.k'
    require(bag([list(r) for r in db.execute(query)]) == bag(oracle['initial']['output_bag']), 'INITIAL_ORACLE_MISMATCH')
    for e in oracle['events']:
        t,row = e['table'],e['row']
        require(t in ('L','R'), 'TABLE')
        if e['operation'] == 'insert':
            db.execute(f'INSERT INTO {t} VALUES ({",".join("?" for _ in row)})', row)
        else:
            require(e['operation'] == 'delete','OPERATION')
            db.execute(f'DELETE FROM {t} WHERE {"lid" if t=="L" else "rid"}=?', [row[0]])
        require(bag([list(r) for r in db.execute(query)]) == bag(e['after']['output_bag']), 'ORACLE_BAG_MISMATCH')
        for t in ('L','R'):
            require(bag([list(r) for r in db.execute(f'SELECT * FROM {t}')]) == bag(e['after'][t+'rows']), 'ORACLE_ROWS_MISMATCH')
    receipts = []
    for call in range(1,7):
        req = read(ROOT / f'requests/{call:04d}.json')
        rec = read(ROOT / f'responses/{call:04d}.json')
        sent = read(ROOT / f'provider/{call:04d}/call-0001.request.json')
        got = read(ROOT / f'provider/{call:04d}/call-0001.response.json')
        raw = (ROOT / f'responses/{call:04d}.txt').read_bytes()
        require(sent['request'] == got['request'] == req['provider_payload'], 'REQUEST_MISMATCH')
        require(got['content'].encode('utf-8') == raw and sha(raw) == rec['text_sha256'], 'ANSWER_MISMATCH')
        require(got['usage'] == rec['usage'], 'USAGE_MISMATCH')
        require(got['status'] == rec['status'] == 'COMPLETE', 'INCOMPLETE')
        require(got['finish_reason'] == rec['finish_reason'] == 'stop', 'FINISH')
        require(got['reasoning_content_persisted'] is False, 'HIDDEN_REASONING')
        receipts.append(dict(call_id=call, public_sha256=sha(raw), provider_identity_equal=True))
    results = []
    for call,events in ((1,oracle['events'][:2]),(4,oracle['events'][2:]),(6,oracle['events'][2:])):
        states = extract(call)
        require(len(states) == len(events), f'STATE_COUNT_CALL_{call}')
        results.extend(compare(call,s,e['after'],f'event_{i+1}') for i,(s,e) in enumerate(zip(states,events)))
    for call in (3,5):
        states = extract(call)
        require(bool(states),'NO_U1_STATE')
        results.append(compare(call,states[-1],oracle['events'][1]['after'],'U1_endpoint'))
    result = dict(schema='minireason.harness.post-observation-finite-check.v1',
        created_utc=datetime.now(timezone.utc).isoformat(),
        method='Authored after observation. Extract every JSON event-state fence after Event1 heading; for U1 choose final state. Bag equality ignores order and preserves duplicates; exact ID indexes are checked. Source fence line numbers recorded.',
        limits='Finite fields and provider custody only. Contradictory prose, parent continuity, attribution, criticism validity and reason-use require separate root review.',
        checker_sha256=sha(Path(__file__).read_bytes()), oracle_sha256=sha(ORACLE.read_bytes()),
        sqlite_version=sqlite3.sqlite_version, oracle_recomputed_equal=True, provider_receipts=receipts,
        event_occurrences_checked=10, u1_endpoints_checked=2, results=results,
        all_finite_fields_equal=all(r['all_equal'] for r in results))
    with (ROOT/'operator-check.json').open('x',encoding='utf-8',newline='\n') as f:
        json.dump(result,f,indent=2,ensure_ascii=False); f.write('\n')
    print(json.dumps({k:result[k] for k in ('oracle_recomputed_equal','event_occurrences_checked','u1_endpoints_checked','all_finite_fields_equal')}))
if __name__ == '__main__': main()

