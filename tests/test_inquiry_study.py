"""Offline inquiry checks; fixtures are instrumentation, not experiment results."""
from pathlib import Path
import hashlib
import json
import re
import tempfile
import unittest
from unittest.mock import patch

from minireason.inquiry_study import (ARMS, STAGES, STAGE_INSTRUCTIONS, _signed, freeze_occurrence,
    make_plan, run_test)
from minireason.provider import write_new


BASE = Path(__file__).resolve().parents[1]


def packet():
    return json.loads((BASE/'experiments/records/E004-paired-languages/packet.json').read_text())


class FakeProvider:
    def __init__(self, settings, root, outputs, fail_stage=None, usage=None):
        self.settings, self.root = settings, root
        self.outputs, self.fail_stage = outputs, fail_stage
        self.usage = {'prompt_tokens': 7, 'completion_tokens': 5} if usage is None else usage
        self.calls = self.prompt_tokens = self.completion_tokens = 0

    def complete(self, messages, *, json_output, coordinate):
        self.calls += 1
        self.prompt_tokens += 7
        self.completion_tokens += 5
        stage = coordinate['stage']
        write_new(self.root/f'call-{self.calls:04d}.request.json',
                  {'messages': messages, 'json_output': json_output, 'coordinate': coordinate})
        if stage == self.fail_stage:
            raise RuntimeError('DELIBERATE_LATE_FAILURE')
        result = {'content': self.outputs[stage], 'usage': self.usage}
        write_new(self.root/f'call-{self.calls:04d}.response.json', result)
        return result


class InquiryStudyTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.packet = packet()
        self.issue = freeze_occurrence('This is a test-only unresolved issue occurrence.\nNo target bearing is established.\n',
            {'experiment': 'OFFLINE_FIXTURE', 'stage': 'criticize', 'artifact': 'fixture-source'}, self.packet['packet_id'])
        self.parent = freeze_occurrence('Exact earlier specimen with λ and trailing newline.\n',
            {'experiment': 'OFFLINE_FIXTURE', 'stage': 'construct'}, self.packet['packet_id'])
        self.outputs = {'construct': 'J: A new, possibly false connection.\n',
            'criticize': 'C_J: The connection may conflate two meanings.\n',
            'revise': "J′ remains a proposal. Its preservation promise is untested.\n",
            'promote': 'No clear successor is justified yet. What issue, if any, does this identify?\n???\n'}

    def make(self, arms=None):
        return make_plan('OFFLINE-INQUIRY', self.packet, self.issue, 'lean_candidate',
            'Instrumentation fixture only; do not infer an experiment selection or substantive lesson.',
            parents=[self.parent], arms=arms)

    def test_all_six_controls_actual_large_material_and_conditional_request_parity(self):
        from minireason.inquiry_mini import compile_manifest
        plan = self.make()
        self.assertGreater(len(plan['packet_text']), 8192)
        self.assertGreater(len(plan['selected_language_text']), 4000)
        write_new(self.root/'plan.json', plan)
        constructed = []
        def factory(settings, path):
            preflight = json.loads((self.root/'run/preflight.json').read_text())
            self.assertEqual(preflight['status'], 'CONFIGURATION_PREFLIGHT_PASSED')
            constructed.append(settings)
            return FakeProvider(settings, path, self.outputs)
        with patch('minireason.inquiry_mini.compile_manifest', wraps=compile_manifest) as compiler:
            summary = run_test(self.root/'plan.json', self.root/'run', jobs=5, provider_factory=factory)
        self.assertEqual(compiler.call_count, 1)
        self.assertEqual(len(constructed), 6)
        self.assertEqual(sum(setting.thinking for setting in constructed), 3)
        self.assertTrue(all(row['status'] == 'OBSERVATIONS_RECORDED' for row in summary['arms']), summary)
        for arm in ARMS:
            expected = 1 if arm in {'bare', 'native'} else 4
            row = next(row for row in summary['arms'] if row['arm'] == arm)
            self.assertEqual(row['resources']['calls'], expected)
            result = json.loads((self.root/f'run/{arm}-r01/result.json').read_text())
            self.assertEqual(result['schema'], 'minireason.inquiry-arm.v1')
            self.assertEqual(result['standing_effect'], 'none')
            self.assertFalse(result['proposed_changes_installed'])
            self.assertEqual([row['text'] for row in result['history']], [self.outputs[s] for s in STAGES[:expected]])
            for index in range(1, expected + 1):
                request = json.loads((self.root/f'run/{arm}-r01/calls/call-{index:04d}.request.json').read_text())
                matched = json.loads((self.root/f'run/matched-r01/calls/call-{index:04d}.request.json').read_text())
                self.assertEqual(request['messages'], matched['messages'])
                self.assertFalse(request['json_output'])
        self.assertEqual(json.loads((self.root/'run/packet.json').read_text()), self.packet)
        self.assertEqual(json.loads((self.root/'run/selected-occurrence.json').read_text()), self.issue)

    def test_whole_promotion_is_queued_without_semantic_extraction_or_successor_installation(self):
        plan = self.make(['matched', 'mini'])
        write_new(self.root/'plan.json', plan)
        run_test(self.root/'plan.json', self.root/'run', provider_factory=lambda settings, path: FakeProvider(settings, path, self.outputs))
        for arm in ('matched', 'mini'):
            queue = json.loads((self.root/f'run/{arm}-r01/inquiry-queue.json').read_text())
            self.assertFalse(queue['automatic_successor_started'])
            self.assertEqual(queue['content_appraisal'], 'unresolved')
            occurrence = queue['occurrences'][0]
            self.assertEqual(occurrence['text'], self.outputs['promote'])
            self.assertEqual(occurrence['text_sha256'], hashlib.sha256(self.outputs['promote'].encode()).hexdigest())
            self.assertEqual(occurrence['disposition'], 'queued')
            self.assertEqual(occurrence['standing_effect'], 'none')
            self.assertNotIn('about', occurrence)
            self.assertNotIn('answers', occurrence)
            self.assertIn(self.issue['occurrence_id'], occurrence['origin']['supplied_input_occurrence_ids'])
            successor = make_plan('OFFLINE-SUCCESSOR', self.packet, occurrence, 'lean_candidate',
                'Ask what issue, if any, the unchanged occurrence identifies.', arms=['bare'])
            self.assertEqual(successor['issue'], occurrence)
            self.assertEqual(successor['activation']['standing_effect'], 'none')

    def test_late_failure_retains_both_prior_occurrences_and_no_manufactured_promotion(self):
        plan = self.make(['matched', 'mini'])
        write_new(self.root/'plan.json', plan)
        run_test(self.root/'plan.json', self.root/'run', provider_factory=lambda settings, path:
            FakeProvider(settings, path, self.outputs, fail_stage='revise'))
        for arm in ('matched', 'mini'):
            result = json.loads((self.root/f'run/{arm}-r01/result.json').read_text())
            self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
            self.assertEqual([row['stage'] for row in result['history']], ['construct', 'criticize'])
            self.assertIn('DELIBERATE_LATE_FAILURE', json.dumps(result['alarms']))
            queue = json.loads((self.root/f'run/{arm}-r01/inquiry-queue.json').read_text())
            self.assertEqual(queue['occurrences'], [])

    def test_malformed_actual_mini_configuration_records_zero_provider_failure_for_every_arm(self):
        plan = self.make(['bare', 'mini'])
        plan['stage_instructions']['promote'] = 'Oversized instruction. ' * 300
        plan = _signed({key: value for key, value in plan.items() if key != 'plan_id'}, 'plan_id')
        write_new(self.root/'plan.json', plan)
        with patch('minireason.inquiry_study.DeepSeek') as factory:
            result = run_test(self.root/'plan.json', self.root/'run', provider_factory=factory)
        factory.assert_not_called()
        self.assertEqual(result['preflight']['status'], 'CONFIGURATION_PREFLIGHT_FAILED')
        self.assertTrue(all(row['resources']['calls'] == 0 for row in result['arms']))
        self.assertIn('MINI_MANIFEST_INVALID', (self.root/'run/errata.json').read_text())
        self.assertTrue((self.root/'run/REPORT.md').is_file())

    def test_exact_original_agenda_prompts_and_no_baked_issue_or_pair(self):
        agenda = (BASE/'docs/RESEARCH_AGENDA.md').read_text()
        headings = {'construct': 'construct_joint', 'criticize': 'criticize_joint',
                    'revise': 'propose_revision', 'promote': 'promote_question'}
        for stage, heading in headings.items():
            expected = re.search(r'### Exact `' + heading + r'` instruction\n\n> ([^\n]+)', agenda).group(1)
            self.assertEqual(STAGE_INSTRUCTIONS[stage], expected)
        first = self.make(['bare'])
        second_issue = freeze_occurrence('A completely different unresolved occurrence.',
            {'experiment': 'OTHER_FIXTURE'}, self.packet['packet_id'])
        second = make_plan('OTHER', self.packet, second_issue, 'prose', 'A different allocation reason.', arms=['bare'])
        self.assertNotEqual(first['issue_text'], second['issue_text'])
        self.assertNotIn('P7', second['issue_text'])
        self.assertNotEqual(first['plan_id'], second['plan_id'])

    def test_rebound_activation_is_refused_before_any_provider(self):
        plan = self.make(['matched', 'mini'])
        plan['activation']['occurrence_id'] = '0' * 64
        # Even a consistently re-signed envelope cannot bind a different selected issue.
        plan['issue_text'] = json.dumps({'occurrence': plan['issue'], 'activation': plan['activation']},
                                       ensure_ascii=False, sort_keys=True, indent=2)
        plan = _signed({key: value for key, value in plan.items() if key != 'plan_id'}, 'plan_id')
        write_new(self.root/'plan.json', plan)
        with patch('minireason.inquiry_study.DeepSeek') as factory:
            result = run_test(self.root/'plan.json', self.root/'run', provider_factory=factory)
        factory.assert_not_called()
        self.assertEqual(result['preflight']['status'], 'CONFIGURATION_PREFLIGHT_FAILED')
        self.assertIn('INQUIRY_ACTIVATION_MISMATCH', (self.root/'run/errata.json').read_text())

    def test_resigned_occurrence_with_false_text_hash_is_not_an_exact_occurrence(self):
        issue = {**self.issue, 'text_sha256': '0' * 64}
        issue = _signed({key: value for key, value in issue.items() if key != 'occurrence_id'}, 'occurrence_id')
        with self.assertRaisesRegex(ValueError, 'OCCURRENCE_TEXT_MISMATCH'):
            make_plan('WRONG-HASH', self.packet, issue, 'prose', 'A stated reason.')

    def test_missing_usage_and_exceeded_completion_cap_stop_both_routes_after_one_call(self):
        for name, usage, code in [('missing', {}, 'INQUIRY_USAGE_UNAVAILABLE'),
                                 ('exceeded', {'prompt_tokens': 7, 'completion_tokens': 20000},
                                  'INQUIRY_COMPLETION_CEILING_VIOLATED')]:
            with self.subTest(name=name):
                plan = self.make(['matched', 'mini'])
                path = self.root/name
                write_new(path/'plan.json', plan)
                run_test(path/'plan.json', path/'run', provider_factory=lambda settings, root:
                         FakeProvider(settings, root, self.outputs, usage=usage))
                for arm in ('matched', 'mini'):
                    result = json.loads((path/f'run/{arm}-r01/result.json').read_text())
                    self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
                    self.assertEqual(result['history'], [])
                    self.assertEqual(result['resources']['calls'], 1)
                    self.assertIn(code, json.dumps(result['alarms']))

    def test_provider_settings_drift_is_refused_before_calls(self):
        from dataclasses import replace
        plan = self.make(['matched', 'mini'])
        write_new(self.root/'plan.json', plan)
        run_test(self.root/'plan.json', self.root/'run', provider_factory=lambda settings, path:
            FakeProvider(replace(settings, thinking=not settings.thinking), path, self.outputs))
        for arm in ('matched', 'mini'):
            result = json.loads((self.root/f'run/{arm}-r01/result.json').read_text())
            self.assertEqual(result['status'], 'OPERATIONAL_FAILURE')
            self.assertEqual(result['resources']['calls'], 0)
            self.assertIn('INQUIRY_PROVIDER_SETTINGS_MISMATCH', json.dumps(result['alarms']))


if __name__ == '__main__':
    unittest.main()
