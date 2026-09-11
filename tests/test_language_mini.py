"""Real Mini execution with free-prose providers and observed stage visibility."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from minireason.language_mini import make_manifest, run_probe
from minireason.language_data import RAW_SYSTEM
from minireason.language_study import stage_prompt
from minireason.provider import ProviderFailure, Settings

PACKET = 'ORIGINAL_CORPUS_SENTINEL\nClaim with an unresolved alternative.\nOTHER_LANGUAGE_SENTINEL'
LANGUAGE = 'SELECTED_LANGUAGE_SENTINEL\nThis candidate may be incomplete and noncomputable.'
PACKET += '\n' + LANGUAGE
COMPILER = 'COMPILER_SENTINEL: the proposed Lean snippet did not elaborate.'
INSTRUCTIONS = {'express': 'Express the frozen material; do not repair its language.',
                'reinterpret': 'Interpret only the expression and the supplied language meaning.',
                'criticize': 'Compare the original, expression and reading. Prose objections are legitimate.'}


class ProseProvider:
    def __init__(self, *, failure_stage=None, cap=2048):
        self.settings = Settings(max_tokens=cap)
        self.failure_stage = failure_stage
        self.requests = []

    def complete(self, messages, *, json_output, coordinate):
        self.requests.append({'messages': messages, 'json_output': json_output, 'coordinate': coordinate})
        stage, cycle = coordinate['stage'], coordinate['cycle']
        if stage == self.failure_stage:
            raise ProviderFailure('OFFLINE_INJECTED_FAILURE', 'The reader observation was not obtained')
        raw = {'express': f'EXPRESSION_CYCLE_{cycle}\nThe expression cannot settle this.\n```not-lean\n???\n```\n',
               'reinterpret': f'READING_CYCLE_{cycle}\nTwo interpretations remain open; neither is proved.\n',
               'criticize': f'CRITICISM_CYCLE_{cycle}\nA prose objection cannot be expressed in the selected formal carrier.\n'}[stage]
        return {'content': raw, 'usage': {'prompt_tokens': 31, 'completion_tokens': 17}}


class LanguageMiniTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.arguments = dict(packet_text=PACKET, selected_language_text=LANGUAGE,
                              carrier_directive='Use the frozen non-Lean class; prose escape is legitimate.',
                              stage_instructions=INSTRUCTIONS, max_tokens=2048, compiler_text=COMPILER)

    def test_wire_inputs_hide_source_only_from_reinterpret_and_restore_all_material_for_criticism(self):
        provider = ProseProvider()
        result = run_probe(provider, self.root, **self.arguments)
        self.assertEqual(result['status'], 'COMPLETE', result['alarms'])
        self.assertEqual([r['coordinate']['stage'] for r in provider.requests], ['express', 'reinterpret', 'criticize'])
        prompts = {r['coordinate']['stage']: r['messages'][-1]['content'] for r in provider.requests}
        self.assertIn(PACKET, prompts['express'])
        self.assertIn(PACKET, prompts['criticize'])
        self.assertNotIn('ORIGINAL_CORPUS_SENTINEL', prompts['reinterpret'])
        self.assertNotIn('OTHER_LANGUAGE_SENTINEL', prompts['reinterpret'])
        self.assertNotIn('## The problem (problem)', prompts['reinterpret'])
        for prompt in prompts.values():
            self.assertIn(LANGUAGE, prompt)
            self.assertNotIn('A JSON object carrying "body" and "commitments"', prompt)
        self.assertIn('EXPRESSION_CYCLE_1', prompts['reinterpret'])
        self.assertIn('EXPRESSION_CYCLE_1', prompts['criticize'])
        self.assertIn('READING_CYCLE_1', prompts['criticize'])
        self.assertNotIn(COMPILER, prompts['express'])
        self.assertNotIn(COMPILER, prompts['reinterpret'])
        self.assertIn(COMPILER, prompts['criticize'])
        self.assertTrue(all(r['json_output'] is False for r in provider.requests))
        self.assertEqual(result['mini_outcome']['calls'], 3)
        self.assertEqual(result['mini_outcome']['stages_entered'], ['express', 'reinterpret', 'criticize'])
        self.assertEqual(result['interpretation_status'], 'NOT_ADJUDICATED')
        self.assertEqual(result['alarms'], [])

    def test_unresolved_noncompiling_prose_survives_losslessly_and_cycles_do_not_install_repairs(self):
        provider = ProseProvider()
        result = run_probe(provider, self.root, cycles=2, **self.arguments)
        self.assertEqual(result['status'], 'COMPLETE', result['alarms'])
        self.assertEqual(result['mini_outcome']['calls'], 6)
        self.assertEqual(result['mini_outcome']['cycles_completed'], 2)
        rows = {(r['stage'], r['cycle']): r for r in result['history']}
        expression = rows['express', 1]['text']
        self.assertEqual(expression, 'EXPRESSION_CYCLE_1\nThe expression cannot settle this.\n```not-lean\n???\n```\n')
        self.assertEqual(rows['express', 1]['answer']['commitments'], expression)
        second_reader = provider.requests[4]['messages'][-1]['content']
        self.assertIn('EXPRESSION_CYCLE_2', second_reader)
        self.assertNotIn('EXPRESSION_CYCLE_1', second_reader)
        second_expression = provider.requests[3]['messages'][-1]['content']
        self.assertIn(PACKET, second_expression)
        self.assertNotIn('CRITICISM_CYCLE_1', second_expression)
        self.assertEqual(json.loads((self.root/'manifest.json').read_text())['problem'], PACKET)
        self.assertEqual(len(result['history']), 6)

    def test_reader_transport_failure_retains_expression_and_loud_terminal_record(self):
        provider = ProseProvider(failure_stage='reinterpret')
        result = run_probe(provider, self.root, **self.arguments)
        self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
        self.assertIsNone(result['final'])
        self.assertEqual([r['stage'] for r in result['history']], ['express'])
        self.assertIn('OFFLINE_INJECTED_FAILURE', {a['code'] for a in result['alarms']})
        self.assertTrue((self.root/'run/log.jsonl').is_file())
        self.assertTrue((self.root/'probe-result.json').is_file())
        self.assertTrue(json.loads((self.root/'probe-errata.json').read_text())['operational'])
        self.assertEqual(len(provider.requests), 2)

    def test_freezing_binds_carrier_meaning_and_packet_without_a_compilation_requirement(self):
        original = make_manifest(**self.arguments)
        for name in ('packet_text', 'selected_language_text', 'carrier_directive', 'compiler_text'):
            changed = make_manifest(**{**self.arguments, name: self.arguments[name] + '\nchanged'})
            self.assertNotEqual(original['manifest_id'], changed['manifest_id'])
        reader = next(k for k in original['kinds'] if k['kind_id'] == 'minireason.language-reading.v1')
        self.assertEqual(reader['input_ports'], [{'port_id': 'expression', 'port_type': 'expression', 'window': 'this_cycle'}])
        self.assertNotIn('sources', original)
        self.assertTrue(all('format' not in kind for kind in original['kinds']))

    def test_cap_mismatch_refuses_without_model_call(self):
        provider = ProseProvider(cap=1024)
        result = run_probe(provider, self.root, **self.arguments)
        self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
        self.assertEqual(provider.requests, [])
        self.assertIn('PROBE_COMPLETION_CAP_MISMATCH', {a['code'] for a in result['alarms']})

    def test_actual_mini_routing_leak_fails_before_the_reader_call(self):
        from creib.forge.mini.runner import render_brief as original
        def leaked(plan, state, blobs, stage, cycle=0):
            text, exposed = original(plan, state, blobs, stage, cycle)
            if stage.stage_id == 'reinterpret':
                text += '\n\nUnexpected source packet:\n' + PACKET
            return text, exposed
        provider = ProseProvider()
        with mock.patch('creib.forge.mini.runner.render_brief', side_effect=leaked):
            result = run_probe(provider, self.root, **self.arguments)
        self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
        self.assertEqual(len(provider.requests), 1)
        self.assertIn('PROBE_ROUTING_MISMATCH', {a['code'] for a in result['alarms']})

    def test_sent_request_policy_matches_direct_renderer_and_host_wrapper_is_separately_accounted(self):
        provider = ProseProvider()
        result = run_probe(provider, self.root, **self.arguments)
        self.assertEqual(result['status'], 'COMPLETE', result['alarms'])
        prior = []
        for request, row in zip(provider.requests, result['history']):
            stage = row['stage']
            self.assertEqual(request['messages'][0], {'role': 'system', 'content': RAW_SYSTEM})
            self.assertEqual(request['messages'][-1]['content'], stage_prompt(self.arguments, stage, prior))
            self.assertTrue(result['visibility'][len(prior)]['complete_routed_brief_verified'])
            transport = json.loads((self.root / 'requests' / f'001-{stage}-transport.json').read_text())
            self.assertFalse(transport['independent_commitment_call'])
            self.assertEqual(transport['provider_completion_tokens'], 17)
            self.assertEqual(transport['raw_text_sha256'], row['text_sha256'])
            self.assertGreater(transport['wrapped_utf8_bytes'], transport['raw_utf8_bytes'])
            self.assertIsNone(transport['wrapper_tokens'])
            prior.append(row)


if __name__ == '__main__':
    unittest.main()
