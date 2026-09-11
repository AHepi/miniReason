"""Offline transport-to-Mini integration; supplied solutions calibrate machinery only."""
from __future__ import annotations

from contextlib import contextmanager
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest import mock

from minireason.campaign import ARMS, make_plan, run_test
from minireason.provider import Settings, write_new
from minireason.templates import TEMPLATES
from tests.test_tasks import correct_program


class CampaignIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.payloads: list[dict] = []
        self.lock = threading.Lock()

    @contextmanager
    def response(self, request, *, timeout):
        if getattr(self, 'fail_transport', False):
            raise OSError('offline injected transport failure')
        payload = json.loads(request.data)
        with self.lock:
            self.payloads.append(payload)
        prompt = payload['messages'][-1]['content']
        critic = any(template['critic'] in prompt for template in TEMPLATES.values())
        answer = {'body': 'Fixture criticism grounded in the supplied contract.' if critic else
                          'Fixture construction: select the latest revision before testing liveness.',
                  'commitments': 'No demonstrated defect; preserve the implementation.' if critic else
                                 json.dumps(correct_program())}
        thinking = payload['thinking']['type'] == 'enabled'
        raw = {'id': 'mock-call', 'model': 'deepseek-flash', 'created': 1,
               'choices': [{'finish_reason': 'stop', 'message': {'content': json.dumps(answer),
                            'reasoning_content': 'TEST_PRIVATE_REASONING_SENTINEL' if thinking else ''}}],
               'usage': {'prompt_tokens': 42, 'completion_tokens': 23}}
        yield io.BytesIO(json.dumps(raw).encode())

    def run_plan(self, *, arms=None, cycles=2, feedback=True, return_path=True):
        with mock.patch.dict(os.environ, {'DEEPSEEK_API_KEY': 'offline-test-key'}), \
             mock.patch('minireason.provider._open', side_effect=self.response), \
             mock.patch('minireason.campaign.source_identity', return_value={'source_sha256': 'offline-test-source'}):
            plan = make_plan('offline-integration', 'critic_revision_v1',
                             'Calibrate transport, execution, wiring and terminal records with a supplied solution.',
                             cycles=cycles, max_tokens=4096, arms=arms,
                             feedback=feedback, return_path=return_path)
            path = self.root / 'plan.json'
            write_new(path, plan)
            summary = run_test(path, self.root / 'run', jobs=5)
        return plan, summary

    def test_all_six_arms_complete_and_mini_records_declared_endpoint_and_cycles(self) -> None:
        plan, summary = self.run_plan()
        self.assertEqual({row['arm'] for row in summary['arms']}, ARMS)
        self.assertEqual(len(self.payloads), 26)
        for arm in ARMS:
            with self.subTest(arm=arm):
                directory = self.root / 'run' / f'{arm}-r01'
                result = json.loads((directory / 'result.json').read_text())
                self.assertEqual(result['status'], 'TASK_SURVIVED', result.get('alarms'))
                self.assertTrue(result['public']['all_pass'])
                self.assertTrue(result['holdout']['all_pass'])
                self.assertEqual(result['resources']['calls'], 1 if arm in {'bare', 'native'} else 6)
                self.assertTrue((directory / 'started.json').is_file())
                errata = json.loads((directory / 'errata.json').read_text())
                self.assertEqual(errata['operational'], [])
                self.assertEqual(errata['candidate_failures'], [])
                if arm.startswith('mini'):
                    outcome = result['mini_outcome']
                    self.assertEqual(outcome['cycles_completed'], 2)
                    self.assertEqual(outcome['stop_reason'], 'cycle_cap')
                    self.assertEqual(outcome['stages_entered'], ['conjecture', 'execute', 'criticise', 'revise'] * 2)
                    events = [json.loads(line) for line in (directory / 'mini/log.jsonl').read_text().splitlines()]
                    self.assertEqual(events[0]['type'], 'RUN_STARTED')
                    self.assertEqual(events[0]['payload']['endpoint'],
                                     Settings(thinking=arm == 'mini_native', max_tokens=4096).to_dict())
                    self.assertEqual(events[-1]['type'], 'RUN_ENDED')
                    self.assertEqual([row['stage'] for row in result['history']],
                                     ['conjecture', 'revise', 'conjecture', 'revise'])
        self.assertEqual(summary['interpretation_status'], 'PENDING_SUBSTANTIVE_REVIEW')
        for path in (self.root / 'run').rglob('*'):
            if path.is_file():
                self.assertNotIn('TEST_PRIVATE_REASONING_SENTINEL', path.read_text())

    def test_mini_and_matched_ablation_keep_terminal_route_without_feedback_or_return(self) -> None:
        _, summary = self.run_plan(arms=['matched', 'mini'], cycles=1, feedback=False, return_path=False)
        self.assertEqual({row['status'] for row in summary['arms']}, {'TASK_SURVIVED'})
        mini = json.loads((self.root / 'run/mini-r01/result.json').read_text())
        self.assertEqual(mini['mini_outcome']['stages_entered'], ['conjecture', 'criticise', 'revise'])
        self.assertEqual(mini['resources']['calls'], 3)

    def test_transport_failure_leaves_a_terminal_result_and_errata_for_every_arm(self) -> None:
        self.fail_transport = True
        _, summary = self.run_plan(cycles=1)
        self.assertEqual(len(summary['arms']), 6)
        self.assertEqual({row['status'] for row in summary['arms']}, {'OPERATIONAL_FAILURE'})
        for arm in ARMS:
            directory = self.root / 'run' / f'{arm}-r01'
            result = json.loads((directory / 'result.json').read_text())
            errata = json.loads((directory / 'errata.json').read_text())
            self.assertTrue(result['ended_at'])
            self.assertTrue(errata['operational'])
            self.assertTrue((directory / 'calls/call-0001.response.json').is_file())
            self.assertEqual(result['resources']['calls'], 1)
            self.assertFalse(result.get('holdout'))

    def test_source_drift_refuses_before_provider_or_records(self) -> None:
        with mock.patch('minireason.campaign.source_identity', return_value={'source_sha256': 'before'}):
            plan = make_plan('drift', 'critic_revision_v1', 'Source identity gate calibration.')
        path = self.root / 'plan.json'
        write_new(path, plan)
        with mock.patch('minireason.campaign.source_identity', return_value={'source_sha256': 'after'}), \
             mock.patch('minireason.provider._open') as transport:
            with self.assertRaisesRegex(ValueError, 'SOURCE_CHANGED_SINCE_PLAN'):
                run_test(path, self.root / 'run')
        transport.assert_not_called()
        self.assertFalse((self.root / 'run').exists())

    def test_cli_help_is_available_without_a_credential(self) -> None:
        completed = subprocess.run([sys.executable, '-m', 'minireason.campaign', '--help'],
                                   capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('plan', completed.stdout)
        self.assertIn('run', completed.stdout)


if __name__ == '__main__':
    unittest.main()
