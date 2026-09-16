from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
maps=json.loads((ROOT/'problems/RECODING_MAPS.json').read_text(encoding='utf-8'))['candidates']
rels={x['candidate_id']:x for x in json.loads((ROOT/'problems/RELATIONS.json').read_text(encoding='utf-8'))['candidates']}
assert [m['candidate_id'] for m in maps]==[f'C{i:02d}' for i in range(1,25)]
results=[]; recoding=[]; carrier=[]
for m in maps:
 cid=m['candidate_id']; p=subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/m['oracle_path'])],cwd=str(ROOT/'oracle'),capture_output=True,text=True,encoding='utf-8',timeout=120,check=True)
 record=json.loads(p.stdout); assert record['candidate_id']==cid and record['expected_match'] and record['trap_rejected']
 assert record['oracle_kind']==m['oracle_kind']
 answer_text=(ROOT/m['answer_path']).read_text(encoding='utf-8'); actual_sealed=json.loads(re.search(r'```json\s*(\{.*?\})\s*```',answer_text,re.S).group(1));assert record['sealed']==actual_sealed
 outpath=ROOT/f'oracle/{cid}.output.json';outpath.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='')
 results.append({'candidate_id':cid,'oracle_kind':record['oracle_kind'],'output_path':f'oracle/{cid}.output.json','output_sha256':hashlib.sha256(outpath.read_bytes()).hexdigest()})
 orig=(ROOT/m['problem_path']).read_text(encoding='utf-8'); rec=(ROOT/m['recoded_problem_path']).read_text(encoding='utf-8'); car=(ROOT/m['carrier_problem_path']).read_text(encoding='utf-8')
 def split(t):
  a,b=t.split('Givens:\n',1); bullets,tail=b.split('\nQuestion:',1);return a,[x for x in bullets.splitlines() if x.strip()],tail
 oh,ob,ot=split(orig);rh,rb,rt=split(rec)
 order=m["forward_order_map"]; assert sorted(order)==list(range(len(ob)))
 assert oh==rh and rb==[ob[i] for i in order] and ot==rt
 assert m["inverse_order_map"]==[order.index(i) for i in range(len(order))]
 assert car==m['carrier_tag']+'\n'+orig
 ids=[x['relation_id'] for x in rels[cid]['relations']];assert ids==m['relation_ids']
 for key in ('problem_path','recoded_problem_path','carrier_problem_path','answer_path','oracle_path'):
  assert hashlib.sha256((ROOT/m[key]).read_bytes()).hexdigest()==m['hashes'][key.replace('_path','_sha256')]
 assert set(m['oracle_support_paths'])==set(m['oracle_support_sha256'])
 for support in m['oracle_support_paths']:
  assert hashlib.sha256((ROOT/support).read_bytes()).hexdigest()==m['oracle_support_sha256'][support]
 recoding.append({'candidate_id':cid,'declared_branch_permutation':True,'question_identity':True,'relation_ids':ids})
 carrier.append({'candidate_id':cid,'payload_identity_after_tag':True})
summary={'status':'PASS','candidate_count':len(results),'computable_count':sum(x['oracle_kind']=='computable' for x in results),'derivation_only_count':sum(x['oracle_kind']=='derivation-only' for x in results),'long_chain_count':sum(bool(x['long_chain']) for x in maps),'results':results,'recoding_checks':recoding,'carrier_checks':carrier}
payload=json.dumps(summary,ensure_ascii=False,separators=(',',':'),sort_keys=True)
(ROOT/'oracle/run_all.output.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='')
print(payload)
