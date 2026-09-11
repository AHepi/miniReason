"""Scratch instrument checks; no network or live model calls."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason.language_data import RAW_SYSTEM
from minireason.provider import Settings, ProviderFailure
from minireason.inquiry_mini import STAGES, prepare_inquiry, run_inquiry


class ProseProvider:
    def __init__(self, failure_stage=None, cap=2048):
        self.settings = Settings(max_tokens=cap)
        self.requests = []
        self.failure_stage = failure_stage

    def complete(self, messages, *, json_output, coordinate):
        self.requests.append(dict(messages=messages, json_output=json_output, coordinate=coordinate))
        stage = coordinate['stage']
        if self.failure_stage == stage:
            raise ProviderFailure('SCRATCH_TRANSPORT_FAILURE', 'This intended occurrence was not obtained')
        raw = f'{stage.upper()}_OCCURRENCE\nUnresolved prose; ??? is not a proof.\n'
        return {'content': raw, 'usage': {'prompt_tokens': 9, 'completion_tokens': 7}}


class InquiryMiniTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.material = dict(packet_text='PACKET_START\n' + 'frozen corpus λ. '*650 + '\nPACKET_END',
            selected_language_text='LANGUAGE_START\n' + 'proposed meaning λ. '*260 + '\nLANGUAGE_END',
            issue_text='ISSUE_START\nThe objection might be irrelevant.\nISSUE_END',
            parent_material_text='PARENTS_START\nActual former occurrence and attributed reason.\nPARENTS_END',
            carrier_directive='Use this frozen proposal; prose criticism is legitimate.',
            stage_instructions={stage: f'Produce the {stage} occurrence without semantic verdict.' for stage in STAGES},
            max_tokens=2048)

    def test_full_sources_and_cumulative_actual_history_match_shared_renderer_without_installed_changes(self):
        from minireason.inquiry_study import stage_prompt
        provider = ProseProvider()
        result = run_inquiry(provider, self.root, **self.material)
        self.assertEqual(result['status'], 'COMPLETE', result['alarms'])
        self.assertEqual(result['mini_outcome']['calls'], 4)
        self.assertEqual(result['mini_outcome']['cycles_completed'], 1)
        self.assertEqual([row['stage'] for row in result['history']], list(STAGES))
        self.assertEqual(result['standing_effect'], 'NONE')
        prior = []
        for index, (request, row) in enumerate(zip(provider.requests, result['history'])):
            self.assertFalse(request['json_output'])
            self.assertEqual(request['messages'][0], {'role': 'system', 'content': RAW_SYSTEM})
            text = request['messages'][-1]['content']
            self.assertEqual(text, stage_prompt(self.material, row['stage'], prior))
            for key in ('packet_text', 'selected_language_text', 'issue_text', 'parent_material_text'):
                self.assertIn(self.material[key], text)
            for earlier in STAGES[:index]:
                self.assertIn(earlier.upper() + '_OCCURRENCE', text)
            for later in STAGES[index:]:
                self.assertNotIn(later.upper() + '_OCCURRENCE', text)
            self.assertEqual(row['text'], row['answer']['body'])
            self.assertEqual(row['text'], row['answer']['commitments'])
            self.assertEqual(row['text_sha256'], hashlib.sha256(row['text'].encode()).hexdigest())
            self.assertFalse(row['proposed_changes_installed'])
            prior.append(row)
        manifest = json.loads((self.root/'manifest.json').read_text())
        self.assertEqual([stage['stage_id'] for stage in manifest['stages'] if stage.get('kind_id') == 'mini.verdict.v1'], ['promote'])
        self.assertNotIn('attention', manifest)
        events = [json.loads(line) for line in (self.root/'run/log.jsonl').read_text().splitlines()]
        artifacts = [event for event in events if event['type'] == 'ARTIFACT_SUBMITTED']
        self.assertEqual(len(artifacts), 8)
        self.assertTrue(all(event['payload']['about'] == [] and event['payload']['answers'] == [] for event in artifacts))
        for source in result['prepared_bindings']['sources']:
            self.assertEqual(hashlib.sha256((self.root/source['path']).read_bytes()).hexdigest(), source['sha256'])

    def test_changed_actual_source_route_stops_before_any_provider_dispatch(self):
        from creib.forge.mini.runner import render_brief as original
        def shortened(plan, state, blobs, stage, cycle=0):
            text, exposed = original(plan, state, blobs, stage, cycle)
            if stage.stage_id == 'construct':
                text = text.replace(self.material['issue_text'], 'shortened')
            return text, exposed
        provider = ProseProvider()
        with mock.patch('creib.forge.mini.runner.render_brief', side_effect=shortened):
            result = run_inquiry(provider, self.root, **self.material)
        self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
        self.assertEqual(provider.requests, [])
        self.assertIn('INQUIRY_ROUTING_MISMATCH', {alarm['code'] for alarm in result['alarms']})
        self.assertTrue((self.root/'requests/001-construct-routed.json').exists())

    def test_missing_criticism_retains_construction_and_does_not_create_successor(self):
        provider = ProseProvider('criticize')
        result = run_inquiry(provider, self.root, **self.material)
        self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
        self.assertEqual([row['stage'] for row in result['history']], ['construct'])
        self.assertIsNone(result['final'])
        self.assertEqual(len(provider.requests), 2)
        self.assertIn('SCRATCH_TRANSPORT_FAILURE', {alarm['code'] for alarm in result['alarms']})
        self.assertTrue((self.root/'inquiry-result.json').exists())
        self.assertTrue((self.root/'inquiry-errata.json').exists())

    def test_two_prepared_issue_routes_are_independent_and_do_not_recompile_during_execution(self):
        from creib.forge.mini.manifest import compile_manifest
        variants = [{**self.material, 'issue_text': self.material['issue_text'] + f'\nUNIQUE_ISSUE_{i}'} for i in range(2)]
        with mock.patch('minireason.inquiry_mini.compile_manifest', wraps=compile_manifest) as compiler:
            prepared = [prepare_inquiry(self.root/f'prepare-{i}', **material) for i, material in enumerate(variants)]
            providers = [ProseProvider(), ProseProvider()]
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(run_inquiry, providers[i], self.root/f'run-{i}', prepared=prepared[i], **variants[i]) for i in range(2)]
                results = [future.result() for future in futures]
            self.assertEqual(compiler.call_count, 2)
        for i, result in enumerate(results):
            self.assertEqual(result['status'], 'COMPLETE', result['alarms'])
            for request in providers[i].requests:
                self.assertIn(f'UNIQUE_ISSUE_{i}', request['messages'][-1]['content'])
                self.assertNotIn(f'UNIQUE_ISSUE_{1-i}', request['messages'][-1]['content'])

    def test_prepared_source_mutation_and_cap_mismatch_are_loud_before_calls(self):
        prepared = prepare_inquiry(self.root/'prepare', **self.material)
        changed = replace(prepared, plan=replace(prepared.plan, sources=(replace(prepared.plan.sources[0], raw=b'altered'),) + prepared.plan.sources[1:]))
        for name, binding, cap, code in [('binding', changed, 2048, 'INQUIRY_PREPARED_PLAN_MISMATCH'),
                                       ('cap', prepared, 1024, 'INQUIRY_COMPLETION_CAP_MISMATCH')]:
            with self.subTest(name=name):
                provider = ProseProvider(cap=cap)
                result = run_inquiry(provider, self.root/name, prepared=binding, **self.material)
                self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
                self.assertEqual(provider.requests, [])
                self.assertIn(code, {alarm['code'] for alarm in result['alarms']})


if __name__ == '__main__':
    unittest.main()
