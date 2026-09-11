"""Offline material-route tests only; scripted prose is not research evidence."""
from dataclasses import replace
from pathlib import Path
import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch

from minireason.reason_use_study import (ARMS,STAGES,_signed,_verify,_settings,freeze_occurrence,
    make_plan,run_test,stage_prompt,reason_use_source_identity)
from minireason.provider import write_new

from minireason import campaign as repository_campaign
REPO = Path(repository_campaign.__file__).resolve().parents[2]


class FixtureProvider:
    def __init__(self,settings,root,outputs,*,fail_stage=None,usage=None):
        self.settings,self.root,self.outputs = settings,root,outputs
        self.fail_stage,self.usage = fail_stage,usage
        self.calls=self.prompt_tokens=self.completion_tokens=0

    def complete(self,messages,*,json_output,coordinate):
        self.calls+=1
        self.prompt_tokens+=7
        self.completion_tokens+=5
        stage=coordinate['stage']
        write_new(self.root/f'call-{self.calls:04d}.request.json',
            {'messages':messages,'json_output':json_output,'coordinate':coordinate})
        if stage==self.fail_stage:
            raise RuntimeError('DELIBERATE_USE_DELIVERY_FAILURE')
        result={'content':self.outputs[stage],
            'usage':{'prompt_tokens':7,'completion_tokens':5} if self.usage is None else self.usage}
        write_new(self.root/f'call-{self.calls:04d}.response.json',result)
        return result


class ReasonUseStudyTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        packet=json.loads((REPO/'experiments/records/E004-paired-languages/packet.json').read_text())
        earlier=(REPO/'experiments/materials/joint-construction-v1/selected-criticism.txt').read_text()
        base=REPO/'experiments/records/E015-joint-prose-retry/mini-r01/calls'
        j=json.loads((base/'call-0001.response.json').read_text())['content']
        r=json.loads((base/'call-0002.response.json').read_text())['content']
        self.texts={'source':json.dumps({'packet':packet,'earlier_E009_criticism':earlier},ensure_ascii=False),
            'construction':j,'original_criticism':r,'criticism':r,
            'use_data':'Minimal use fixture data: marker DELTA_CONTEXT and no historical occurrence.',
            'use_questions':'What does the proposed account license for this declared fixture?'}
        self.outputs={'respond':' Proposed account φ.\nThe fixture remains disputed.\n',
                      'use':'The returned account leaves this fixture unresolved.\n???\n'}

    def inputs(self):
        return {k:freeze_occurrence(v,{'kind':'offline_instrumentation_fixture','field':k},allow_empty=k=='criticism')
                for k,v in self.texts.items()}

    def plan(self,arms=None,relation='original',return_path=True):
        return make_plan('OFFLINE-REASON-USE',self.inputs(),relation,'Exercise routing only.',arms=arms,max_tokens=32768,return_path=return_path)

    def run_plan(self,plan,*,factory=None,folder='run'):
        plan_path=self.root/(folder+'-plan.json')
        write_new(plan_path,plan)
        result=run_test(plan_path,self.root/folder,provider_factory=factory or
            (lambda settings,path:FixtureProvider(settings,path,self.outputs)))
        return result,self.root/folder

    def test_six_controls_with_real_large_packet_mini_and_exact_conditional_parity(self):
        from minireason.reason_use_mini import compile_manifest
        plan=self.plan()
        self.assertGreater(len(plan['source_text']),40000)
        made=[]
        def factory(settings,path):
            made.append(settings)
            self.assertEqual(json.loads((path.parents[1]/'preflight.json').read_text())['status'],'CONFIGURATION_PREFLIGHT_PASSED')
            return FixtureProvider(settings,path,self.outputs)
        with patch('minireason.reason_use_mini.compile_manifest',wraps=compile_manifest) as compiler:
            summary,root=self.run_plan(plan,factory=factory)
        self.assertEqual(compiler.call_count,1)
        self.assertEqual(len(made),6)
        self.assertEqual(sum(s.thinking for s in made),3)
        self.assertTrue(all(a['status']=='OBSERVATIONS_RECORDED' for a in summary['arms']),summary)
        for arm in ARMS:
            expected=1 if arm in {'bare','native'} else 2
            result=json.loads((root/f'{arm}-r01/result.json').read_text())
            self.assertEqual(result['resources']['calls'],expected)
            self.assertEqual(result['standing_effect'],'none')
            self.assertFalse(result['proposed_changes_installed'])
            self.assertEqual([r['text'] for r in result['history']],[self.outputs[s] for s in STAGES[:expected]])
            for index in range(1,expected+1):
                got=json.loads((root/f'{arm}-r01/calls/call-{index:04d}.request.json').read_text())
                control=json.loads((root/f'matched-r01/calls/call-{index:04d}.request.json').read_text())
                self.assertEqual(got['messages'],control['messages'])
                self.assertFalse(got['json_output'])
            for row in result['history']:
                _verify(row,'occurrence_id')
                self.assertNotIn('about',row)
                self.assertNotIn('answers',row)
            if expected==2:
                use=json.loads((root/f'{arm}-r01/calls/call-0002.request.json').read_text())['messages'][1]['content']
                for key in ('source','construction','original_criticism','criticism'):
                    self.assertNotIn(self.texts[key],use)
                self.assertIn(self.outputs['respond'],use)
                provenance=result['history'][1]['origin']['supplied_input_occurrence_ids']
                self.assertNotIn(plan['inputs']['construction']['occurrence_id'],provenance)
                self.assertNotIn(plan['inputs']['criticism']['occurrence_id'],provenance)
                self.assertNotIn(plan['inputs']['source']['occurrence_id'],provenance)
                self.assertIn(result['history'][0]['occurrence_id'],provenance)
                if arm.startswith('mini'):
                    routed=json.loads((root/f'{arm}-r01/requests/001-use-routed.json').read_text())
                    for key in ('source','construction','original_criticism','criticism'):
                        self.assertNotIn(self.texts[key],routed['mini_brief'])

    def test_omission_reaches_actual_mini_as_empty_field(self):
        self.texts['criticism']=''
        plan=self.plan(['matched','mini'],relation='omitted')
        summary,root=self.run_plan(plan)
        self.assertTrue(all(a['status']=='OBSERVATIONS_RECORDED' for a in summary['arms']),summary)
        direct=json.loads((root/'matched-r01/calls/call-0001.request.json').read_text())['messages']
        mini=json.loads((root/'mini-r01/calls/call-0001.request.json').read_text())['messages']
        self.assertEqual(direct,mini)
        self.assertTrue(direct[1]['content'].endswith('Supplemental criticism:\n'))
        self.assertNotIn(self.texts['original_criticism'],direct[1]['content'])

    def test_each_variant_changes_only_response_critic_position_and_not_use_policy(self):
        original=self.plan(['matched'])
        self.texts['criticism']='A separately attributed candidate reason recoding; its equivalence is not certified.'
        recoded=self.plan(['matched'],relation='recoded')
        o=stage_prompt(original,'respond',[])
        r=stage_prompt(recoded,'respond',[])
        self.assertEqual(o.replace(original['criticism_text'],'SELECTED_FIELD'),r.replace(recoded['criticism_text'],'SELECTED_FIELD'))
        history=[{'stage':'respond','text':'Identical fixture account'}]
        self.assertEqual(stage_prompt(original,'use',history),stage_prompt(recoded,'use',history))

    def test_original_criticism_in_json_source_or_use_data_is_refused(self):
        for field in ('source','use_data'):
            with self.subTest(field=field):
                backup=self.texts[field]
                self.texts[field]=json.dumps({'hidden_history':self.texts['original_criticism'],'fraction':0.5})
                with self.assertRaisesRegex(ValueError,'REASON_USE_INPUT_LEAKAGE'):
                    self.plan()
                self.texts[field]=backup

    def test_declared_excerpt_leakage_is_refused_but_unrelated_earlier_critic_is_common(self):
        inputs=self.inputs()
        self.assertIn('earlier_E009_criticism',self.plan()['source_text'])
        snippet='A UNIQUE CRITIC EXCERPT LONG ENOUGH FOR THE DECLARED GUARD.'
        inputs['source']=freeze_occurrence(self.texts['source']+'\n'+snippet,{'kind':'fixture'})
        with self.assertRaisesRegex(ValueError,'REASON_USE_INPUT_LEAKAGE'):
            make_plan('EXCERPT',inputs,'original','Fixture only',literal_exclusions=[{'name':'selected_excerpt','text':snippet}])

    def test_use_rejects_extra_history_and_never_reads_original_fields(self):
        plan=self.plan(['matched'])
        for history in ([],[{'stage':'respond','text':'x'},{'stage':'criticize','text':'hidden'}]):
            with self.assertRaisesRegex(ValueError,'EXACT_RESPONSE_HISTORY'):
                stage_prompt(plan,'use',history)
        minimal={key:plan[key] for key in ('stage_instructions','use_data_text','use_questions_text')}
        prompt=stage_prompt(minimal,'use',[{'stage':'respond','text':'ACCOUNT'}])
        self.assertIn('ACCOUNT',prompt)
        with self.assertRaisesRegex(ValueError,'RESPOND_HISTORY_FORBIDDEN'):
            stage_prompt(plan,'respond',[{'stage':'respond','text':'prior'}])

    def test_failure_after_response_preserves_signed_response_and_makes_no_retry(self):
        summary,root=self.run_plan(self.plan(['matched','mini']),factory=lambda settings,path:
            FixtureProvider(settings,path,self.outputs,fail_stage='use'))
        for arm in ('matched','mini'):
            row=json.loads((root/f'{arm}-r01/result.json').read_text())
            self.assertEqual(row['status'],'OPERATIONAL_FAILURE')
            self.assertEqual(row['resources']['calls'],2)
            self.assertEqual([x['stage'] for x in row['history']],['respond'])
            _verify(row['history'][0],'occurrence_id')
            self.assertIn('DELIBERATE_USE_DELIVERY_FAILURE',json.dumps(row['alarms']))
            self.assertFalse((root/f'{arm}-r01/use.artifact.json').exists())

    def test_missing_usage_and_completion_overrun_stop_after_one_call(self):
        for index,usage in enumerate(({}, {'prompt_tokens':7,'completion_tokens':40000})):
            summary,root=self.run_plan(self.plan(['matched','mini']),folder='bad'+str(index),factory=lambda settings,path:
                FixtureProvider(settings,path,self.outputs,usage=usage))
            for arm in ('matched','mini'):
                row=json.loads((root/f'{arm}-r01/result.json').read_text())
                self.assertEqual(row['status'],'OPERATIONAL_FAILURE')
                self.assertEqual(row['resources']['calls'],1)
                self.assertEqual(row['history'],[])

    def test_provider_setting_drift_is_refused_before_any_call(self):
        summary,root=self.run_plan(self.plan(['matched','mini']),factory=lambda settings,path:
            FixtureProvider(replace(settings,thinking=not settings.thinking),path,self.outputs))
        for row in summary['arms']:
            self.assertEqual(row['resources']['calls'],0)
            self.assertEqual(row['status'],'OPERATIONAL_FAILURE')

    def test_resigned_plan_cannot_rebind_raw_source_or_resource_settings(self):
        for index,field in enumerate(('source_text','settings')):
            plan=self.plan(['matched','mini'])
            if field=='source_text':
                plan[field]+=' altered outside occurrence'
            else:
                plan[field]['temperature']='0.5'
            plan=_signed({k:v for k,v in plan.items() if k!='plan_id'},'plan_id')
            with patch('minireason.reason_use_study.DeepSeek') as factory:
                summary,root=self.run_plan(plan,folder='changed'+str(index),factory=factory)
            factory.assert_not_called()
            self.assertEqual(summary['preflight']['status'],'CONFIGURATION_PREFLIGHT_FAILED')

    def test_source_bytes_drift_blocks_but_publication_commit_alone_does_not(self):
        plan=self.plan(['bare'])
        current=reason_use_source_identity()
        changed=json.loads(json.dumps(current));changed['probe_modules']['reason_use_study.py']='0'*64
        with patch('minireason.reason_use_study.reason_use_source_identity',return_value=changed):
            with patch('minireason.reason_use_study.DeepSeek') as factory:
                summary,_=self.run_plan(plan,folder='source-drift',factory=factory)
        self.assertEqual(summary['preflight']['status'],'CONFIGURATION_PREFLIGHT_FAILED')
        factory.assert_not_called()
        advanced=json.loads(json.dumps(current));advanced['repository']['git_commit']='1'*40
        with patch('minireason.reason_use_study.reason_use_source_identity',return_value=advanced):
            summary,_=self.run_plan(plan,folder='publication-only')
        self.assertEqual(summary['arms'][0]['status'],'OBSERVATIONS_RECORDED',summary)

    def test_preflight_failure_records_zero_calls_and_preserves_frozen_plan(self):
        plan=self.plan(['bare','mini'])
        plan['stage_instructions']['use']='oversized stage instruction '*400
        plan['prompt_policy_sha256']='deliberately unbound'
        plan=_signed({k:v for k,v in plan.items() if k!='plan_id'},'plan_id')
        with patch('minireason.reason_use_study.DeepSeek') as factory:
            summary,root=self.run_plan(plan,factory=factory)
        factory.assert_not_called()
        self.assertEqual(summary['preflight']['status'],'CONFIGURATION_PREFLIGHT_FAILED')
        self.assertTrue(all(row['resources']['calls']==0 for row in summary['arms']))
        self.assertEqual(json.loads((root/'plan.json').read_text()),plan)
        self.assertTrue((root/'REPORT.md').is_file())

    def test_response_carriage_of_prior_content_is_preserved_not_censored(self):
        self.outputs['respond']=self.texts['criticism']+'\nNew proposed account is still disputed.\n'
        summary,root=self.run_plan(self.plan(['matched','mini']))
        self.assertTrue(all(a['status']=='OBSERVATIONS_RECORDED' for a in summary['arms']),summary)
        for arm in ('matched','mini'):
            use=json.loads((root/f'{arm}-r01/calls/call-0002.request.json').read_text())['messages'][1]['content']
            self.assertIn(self.outputs['respond'],use)
            self.assertEqual(use.count(self.texts['criticism']),1)

    def test_no_return_matches_present_except_account_and_uses_actual_mini_without_response_port(self):
        present=self.plan(['matched','mini'])
        absent=self.plan(['matched','mini'],return_path=False)
        yes,yes_root=self.run_plan(present,folder='present')
        no,no_root=self.run_plan(absent,folder='absent')
        self.assertTrue(all(a['status']=='OBSERVATIONS_RECORDED' for a in yes['arms']+no['arms']))
        self.assertEqual(present['stage_instructions'],absent['stage_instructions'])
        self.assertEqual(stage_prompt(present,'respond',[]),stage_prompt(absent,'respond',[]))
        for arm in ('matched','mini'):
            with_account=json.loads((yes_root/f'{arm}-r01/calls/call-0002.request.json').read_text())['messages']
            without_account=json.loads((no_root/f'{arm}-r01/calls/call-0002.request.json').read_text())['messages']
            expected=json.loads(json.dumps(with_account))
            self.assertTrue(expected[1]['content'].endswith(self.outputs['respond']))
            expected[1]['content']=expected[1]['content'][:-len(self.outputs['respond'])]
            self.assertEqual(expected,without_account)
            self.assertTrue(without_account[1]['content'].endswith('Returned account:\n'))
            row=json.loads((no_root/f'{arm}-r01/result.json').read_text())
            self.assertFalse(row['return_path'])
            self.assertEqual(row['resources']['calls'],2)
            self.assertEqual([item['stage'] for item in row['history']],list(STAGES))
            self.assertEqual(row['history'][0]['text'],self.outputs['respond'])
            exposure=row['history'][1]['origin']['supplied_input_occurrence_ids']
            self.assertEqual(exposure,[absent['inputs'][key]['occurrence_id'] for key in ('use_data','use_questions')])
            self.assertNotIn(row['history'][0]['occurrence_id'],exposure)
            self.assertEqual(row['history'][1]['origin']['prompt_sha256'],hashlib.sha256(without_account[1]['content'].encode()).hexdigest())
        direct=json.loads((no_root/'matched-r01/calls/call-0002.request.json').read_text())['messages']
        mini=json.loads((no_root/'mini-r01/calls/call-0002.request.json').read_text())['messages']
        self.assertEqual(direct,mini)
        route=json.loads((no_root/'mini-r01/requests/001-use.json').read_text())
        self.assertFalse(route['actual_response_port_visible'])
        self.assertEqual(route['history_stages_visible'],[])
        self.assertNotIn(self.outputs['respond'],route['mini_brief'])
        manifest=json.loads((no_root/'mini-r01/manifest.json').read_text())
        self.assertEqual(next(s for s in manifest['stages'] if s['stage_id']=='use')['ports'],['use_data','use_questions'])

    def test_no_return_mode_is_frozen_and_rejects_response_history(self):
        plan=self.plan(['matched','mini'],return_path=False)
        with self.assertRaisesRegex(ValueError,'NO_RETURN_HISTORY_FORBIDDEN'):
            stage_prompt(plan,'use',[{'stage':'respond','text':self.outputs['respond']}])
        for invalid in (0,1,'false',None):
            with self.subTest(invalid=invalid),self.assertRaisesRegex(ValueError,'RETURN_PATH_MUST_BE_BOOLEAN'):
                self.plan(return_path=invalid)
        plan['return_path']=True
        plan=_signed({k:v for k,v in plan.items() if k!='plan_id'},'plan_id')
        with patch('minireason.reason_use_study.DeepSeek') as factory:
            result,_=self.run_plan(plan,factory=factory)
        factory.assert_not_called()
        self.assertEqual(result['preflight']['status'],'CONFIGURATION_PREFLIGHT_FAILED')

    def test_no_return_failed_use_keeps_first_response_and_has_no_automatic_retry(self):
        result,root=self.run_plan(self.plan(['matched','mini'],return_path=False),factory=lambda settings,path:
            FixtureProvider(settings,path,self.outputs,fail_stage='use'))
        for arm in ('matched','mini'):
            row=json.loads((root/f'{arm}-r01/result.json').read_text())
            self.assertEqual(row['status'],'OPERATIONAL_FAILURE')
            self.assertEqual(row['resources']['calls'],2)
            self.assertEqual([x['stage'] for x in row['history']],['respond'])
            self.assertEqual(row['history'][0]['text'],self.outputs['respond'])


if __name__=='__main__':
    unittest.main()
