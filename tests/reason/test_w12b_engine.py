"""Offline resilience fixtures retained under work/review12b/engine-tests."""
import contextlib
import copy
import json
from pathlib import Path
import unittest
from unittest import mock
import uuid

from tests.reason import test_engine as fixture
from minireason.reason import config, engine
from minireason.reason.types import ReasonFailure

EVIDENCE = Path(__file__).resolve().parents[2] / 'work/review12b/engine-tests/e'


def length_reply():
    return {'content': '', 'finish_reason': 'length',
            'usage': {'prompt_tokens': 9, 'completion_tokens': 32768,
                      'total_tokens': 32777, 'completion_tokens_details': {'reasoning_tokens': 32768}}}


class ResilienceEngineTests(unittest.TestCase):
    def setUp(self):
        self.case = EVIDENCE / uuid.uuid4().hex[:8]
        self.case.mkdir(parents=True)
        fixture.write(self.case / 'CASE.txt', self.id() + '\n')
        self.counter = fixture.ProviderCounter()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(mock.patch('os.environ', {'PYTHONUTF8': '1'}))
        self.stack.enter_context(fixture.no_network(self.counter))

    tearDown = fixture.OfflineEngineTests.tearDown

    def new_run(self, **kwargs):
        options = {'problem': 'Preserve an invariant across a named boundary.', 'cycles': 1,
                   'out': self.case / 'r', 'mode': 'offline', 'recipe': 'single-family'}
        options.update(kwargs)
        return engine.create_run(**options)

    def native_rival_recipe(self):
        recipe = copy.deepcopy(config.load_recipe('single-family')['data'])
        recipe['name'] = 'offline-native-rival'
        recipe['seats']['rival'] = copy.deepcopy(recipe['seats']['conjecture'])
        path = self.case / 'native-rival.json'
        fixture.write(path, json.dumps(recipe, indent=2) + '\n')
        return path

    def records(self, run):
        return {str(p.relative_to(run)): fixture.read(p)
                for p in (run / 'calls').rglob('*') if p.is_file()}

    def test_new_policy_and_per_mode_ceiling_effort_reach_provider_wire(self):
        run = self.new_run(recipe='cross-family-rival', baseline=True)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(fixture.load(run / 'config.json')['resilience_policy'], 'reasoning-exposure-v2')
        self.assertEqual(state['calls'], 8)
        expected = {'base-bare': 8192, 'base-native': 32768, 'initial': 32768,
                    'c0001-rival': 8192, 'c0001-k01': 8192, 'c0001-k02': 8192,
                    'c0001-return': 32768, 'c0001-use': 8192}
        report = fixture.read(run / 'RUN.md')
        for cid, cap in expected.items():
            with self.subTest(call=cid):
                folder = run / 'calls' / cid / 'a00'
                request = fixture.load(folder / 'request.json')
                prepared = request['prepared']
                self.assertEqual(prepared['kwargs']['max_tokens'], cap)
                self.assertEqual(prepared['kwargs']['reasoning_effort'], 'medium')
                provider = fixture.load(folder / 'provider/call-0001.request.json')
                wire = json.loads(provider['wire_body_text'])
                self.assertEqual(wire, prepared['payload'])
                if prepared['endpoint']['native']:
                    self.assertEqual(wire['options']['num_predict'], cap)
                    self.assertFalse(wire['think'])
                else:
                    self.assertEqual(wire['max_tokens'], cap)
                    if request['thinking'] == 'native':
                        self.assertEqual(wire['reasoning_effort'], 'medium')
                self.assertIn(cid, report)
        bare = fixture.load(run / 'calls/base-bare/a00/request.json')['prepared']
        native = fixture.load(run / 'calls/base-native/a00/request.json')['prepared']
        self.assertEqual(bare['messages'], native['messages'])
        self.assertIn('32768', report)
        self.assertIn('8192', report)
        self.assertIn('medium', report)

    def test_each_baseline_failure_is_recorded_and_does_not_stop_loop(self):
        for label in ('bare', 'native'):
            for failure in ('CEILING_HIT', 'TRANSPORT_OR_RESPONSE_ERROR', 'SCHEMA_FAILURE'):
                with self.subTest(label=label, failure=failure):
                    run = self.new_run(out=self.case / (label + '-' + failure[:3]), baseline=True)
                    original = engine.Adapter.call
                    def inject(adapter, **kwargs):
                        if kwargs['coordinate']['call_id'] == 'base-' + label:
                            if failure == 'SCHEMA_FAILURE':
                                kwargs['scripted'] = {'content': 'Invalid public baseline object.'}
                            elif failure == 'CEILING_HIT':
                                kwargs['scripted'] = length_reply()
                            else:
                                raise ReasonFailure(failure, 'Offline baseline transport fixture')
                        return original(adapter, **kwargs)
                    with mock.patch.object(engine.Adapter, 'call', inject):
                        state = engine.execute(run, scripted=fixture.scripted_reply)
                    self.assertEqual(state['stop_reason'], 'cycle_budget')
                    self.assertEqual(state['completed_cycles'], 1)
                    self.assertTrue((run / 'calls/c0001-use/a00/response.json').exists())
                    for filename in ('BASELINE.md', 'RUN.md'):
                        report = fixture.read(run / filename)
                        self.assertIn(label, report)
                        self.assertIn(failure, report)
                    baseline_requests = list((run / 'calls' / ('base-' + label)).glob('a*/request.json'))
                    for path in baseline_requests:
                        self.assertFalse(fixture.load(path).get('ceiling_fallback'))
                    before = self.records(run)
                    prior = self.counter.offline
                    resumed = engine.execute(run, scripted=fixture.scripted_reply)
                    self.assertEqual(resumed['stop_reason'], 'cycle_budget')
                    self.assertEqual(self.counter.offline, prior)
                    self.assertEqual(self.records(run), before)

    def test_every_native_loop_role_gets_exactly_one_off_fallback_with_same_context(self):
        recipe = self.native_rival_recipe()
        calls = {'conjecture': 'initial', 'rival': 'c0001-rival', 'critic': 'c0001-k01',
                 'return': 'c0001-return', 'use': 'c0001-use'}
        for target, cid in calls.items():
            with self.subTest(role=target):
                count = 0
                def reply(role, cycle, objections):
                    nonlocal count
                    if role == target:
                        count += 1
                        if count == 1:
                            return length_reply()
                    return fixture.scripted_reply(role, cycle, objections)
                run = self.new_run(recipe=recipe, out=self.case / target)
                state = engine.execute(run, scripted=reply)
                self.assertEqual(state['stop_reason'], 'cycle_budget')
                self.assertEqual(state['calls'], 6)
                original = fixture.load(run / 'calls' / cid / 'a00/request.json')
                fallback = fixture.load(run / 'calls' / cid / 'a01/request.json')
                outcome = fixture.load(run / 'calls' / cid / 'a01/response.json')
                self.assertEqual(original['thinking'], 'native')
                self.assertEqual(fallback['thinking'], 'off')
                self.assertEqual(fallback['prepared']['kwargs']['max_tokens'], 32768)
                self.assertEqual(fallback['prepared']['messages'], original['prepared']['messages'])
                self.assertTrue(fallback['ceiling_fallback'])
                self.assertTrue(outcome['ceiling_fallback'])
                self.assertFalse((run / 'calls' / cid / 'a02').exists())
                for name in ('TRACE.md', 'RUN.md'):
                    report = fixture.read(run / name)
                    self.assertIn(cid, report)
                    self.assertIn('fallback', report.lower())
                    self.assertIn('off', report)
                before = self.records(run)
                prior = self.counter.offline
                resumed = engine.execute(run, scripted=reply)
                self.assertEqual(resumed['calls'], 6)
                self.assertEqual(self.counter.offline, prior)
                self.assertEqual(self.records(run), before)

    def test_fallback_failure_is_terminal_even_with_schema_or_transport_retry_allowance(self):
        for failure in ('CEILING_HIT', 'SCHEMA_FAILURE', 'TRANSPORT_OR_RESPONSE_ERROR'):
            with self.subTest(failure=failure):
                count = 0
                def reply(role, cycle, objections):
                    nonlocal count
                    count += 1
                    if count == 1 or failure == 'CEILING_HIT':
                        return length_reply()
                    if failure == 'SCHEMA_FAILURE':
                        return {'content': 'Invalid fallback public object.'}
                    raise ReasonFailure(failure, 'Offline fallback transport fixture')
                run = self.new_run(out=self.case / failure[:3], retry_transport=4)
                state = engine.execute(run, scripted=reply)
                self.assertEqual(state['stop_reason'], failure)
                self.assertEqual(state['calls'], 2)
                self.assertEqual(count, 2)
                self.assertFalse((run / 'calls/initial/a02').exists())
                outcome = fixture.load(run / 'calls/initial/a01/response.json')
                self.assertEqual(outcome['status'], failure)
                self.assertTrue(outcome['ceiling_fallback'])
                self.assertIn('fallback', fixture.read(run / 'TRACE.md').lower())

    def test_off_and_gateway_ceiling_failures_have_no_fallback(self):
        for thinking, endpoint in (('off', 'deepseek-flash'), ('gateway-default', 'ollama/qwen3.5-397b')):
            with self.subTest(thinking=thinking):
                recipe = copy.deepcopy(config.load_recipe('single-family')['data'])
                recipe['seats']['conjecture'] = {'endpoint': endpoint, 'thinking': thinking,
                                                 'reasoning_effort': 'medium'}
                recipe.pop('lineages', None)
                source = self.case / (thinking + '.json')
                fixture.write(source, json.dumps(recipe, indent=2) + '\n')
                run = self.new_run(recipe=source, out=self.case / thinking)
                state = engine.execute(run, scripted=lambda *args: length_reply())
                self.assertEqual(state['stop_reason'], 'CEILING_HIT')
                self.assertEqual(state['calls'], 1)
                self.assertFalse((run / 'calls/initial/a01').exists())

    def test_native_schema_repair_ceiling_allows_fallback_of_that_exact_repair_context(self):
        count = 0
        def reply(role, cycle, objections):
            nonlocal count
            if role == 'conjecture':
                count += 1
                if count == 1:
                    return {'content': 'Public answer missing its JSON object.'}
                if count == 2:
                    return length_reply()
            return fixture.scripted_reply(role, cycle, objections)
        run = self.new_run()
        state = engine.execute(run, scripted=reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['calls'], 6)
        repair = fixture.load(run / 'calls/initial/a01/request.json')
        fallback = fixture.load(run / 'calls/initial/a02/request.json')
        self.assertTrue(repair['schema_repair'])
        self.assertTrue(fallback['ceiling_fallback'])
        self.assertEqual(fallback['thinking'], 'off')
        self.assertEqual(repair['prepared']['messages'], fallback['prepared']['messages'])
        self.assertEqual(fallback['prepared']['kwargs']['max_tokens'], 32768)
        self.assertFalse((run / 'calls/initial/a03').exists())
        self.assertIn('Schema repair calls: 1', fixture.read(run / 'RUN.md'))

    def test_resume_after_native_ceiling_dispatches_only_declared_fallback(self):
        class Interrupted(BaseException):
            pass
        def stop(cid, outcome):
            if cid == 'initial':
                raise Interrupted()
        run = self.new_run()
        with self.assertRaises(Interrupted):
            engine.execute(run, scripted=lambda *args: length_reply(), after_call=stop)
        original = self.records(run)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['calls'], 5)
        self.assertEqual(self.counter.offline, 5)
        for path, text in original.items():
            self.assertEqual(fixture.read(run / path), text)
        self.assertTrue(fixture.load(run / 'calls/initial/a01/request.json')['ceiling_fallback'])

    def test_ambiguous_fallback_intent_is_never_replayed(self):
        class Interrupted(BaseException):
            pass
        original = engine.Adapter.call
        def interrupt(adapter, **kwargs):
            if kwargs['coordinate'].get('ceiling_fallback'):
                raise Interrupted()
            return original(adapter, **kwargs)
        run = self.new_run()
        with mock.patch.object(engine.Adapter, 'call', interrupt):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=lambda *args: length_reply())
        self.assertEqual(self.counter.offline, 1)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'INTERRUPTED_CALL')
        self.assertEqual(self.counter.offline, 1)
        self.assertEqual(state['calls'], 2)
        self.assertFalse((run / 'calls/initial/a01/response.json').exists())
        self.assertFalse((run / 'calls/initial/a02').exists())

    def test_fallback_provider_response_recovers_without_redispatch(self):
        class Interrupted(BaseException):
            pass
        count = 0
        def reply(role, cycle, objections):
            nonlocal count
            if role == 'conjecture':
                count += 1
                if count == 1:
                    return length_reply()
            return fixture.scripted_reply(role, cycle, objections)
        original = engine.Adapter.call
        def interrupt(adapter, **kwargs):
            result = original(adapter, **kwargs)
            if kwargs['coordinate'].get('ceiling_fallback'):
                raise Interrupted()
            return result
        run = self.new_run()
        with mock.patch.object(engine.Adapter, 'call', interrupt):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=reply)
        folder = run / 'calls/initial/a01'
        observed = fixture.read(folder / 'provider/call-0001.response.json')
        self.assertFalse((folder / 'response.json').exists())
        self.assertEqual(self.counter.offline, 2)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['calls'], 5)
        self.assertEqual(self.counter.offline, 5)
        self.assertEqual(fixture.read(folder / 'provider/call-0001.response.json'), observed)
        self.assertTrue(fixture.load(folder / 'response.json')['ceiling_fallback'])

    def legacy_run(self, **kwargs):
        recipe = copy.deepcopy(config.load_recipe('single-family')['data'])
        recipe['ceilings']['native_completion_tokens'] = 8192
        for seat in [recipe['seats']['conjecture'], recipe['seats']['use'], *recipe['seats']['critics']]:
            seat.pop('reasoning_effort', None)
        path = self.case / 'legacy-recipe.json'
        fixture.write(path, json.dumps(recipe, indent=2) + '\n')
        run = self.new_run(recipe=path, **kwargs)
        cfg = fixture.load(run / 'config.json')
        cfg.pop('resilience_policy', None)
        fixture.write(run / 'config.json', json.dumps(cfg, indent=2) + '\n')
        return run

    def test_legacy_frozen_recipe_keeps_ceiling_effort_and_completed_resume(self):
        run = self.legacy_run(baseline=True)
        frozen = {name: fixture.read(run / name) for name in ('recipe.json', 'config.json')}
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['calls'], 6)
        for request in (run / 'calls').glob('*/a*/request.json'):
            kwargs = fixture.load(request)['prepared']['kwargs']
            self.assertEqual(kwargs['max_tokens'], 8192)
            self.assertEqual(kwargs['reasoning_effort'], 'high')
        before = self.records(run)
        prior = self.counter.offline
        resumed = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(resumed['stop_reason'], 'cycle_budget')
        self.assertEqual(self.counter.offline, prior)
        self.assertEqual(self.records(run), before)
        for name, text in frozen.items():
            self.assertEqual(fixture.read(run / name), text)

    def test_legacy_baseline_and_loop_ceiling_failures_remain_fatal_without_fallback(self):
        for baseline in (False, True):
            with self.subTest(baseline=baseline):
                run = self.legacy_run(baseline=baseline, out=self.case / str(baseline))
                state = engine.execute(run, scripted=lambda *args: length_reply())
                self.assertEqual(state['stop_reason'], 'CEILING_HIT')
                self.assertEqual(state['completed_cycles'], 0)
                self.assertEqual(state['calls'], 1)
                cid = 'base-bare' if baseline else 'initial'
                self.assertFalse((run / 'calls' / cid / 'a01').exists())


    def test_baseline_schema_exception_without_public_result_is_nonfatal(self):
        for label in ('bare', 'native'):
            with self.subTest(label=label):
                run = self.new_run(baseline=True, out=self.case / label)
                original = engine.Adapter.call
                def inject(adapter, **kwargs):
                    if kwargs['coordinate']['call_id'] == 'base-' + label:
                        raise ReasonFailure('SCHEMA_FAILURE', 'Offline schema failure without public result')
                    return original(adapter, **kwargs)
                with mock.patch.object(engine.Adapter, 'call', inject):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'cycle_budget')
                self.assertEqual(state['completed_cycles'], 1)
                self.assertEqual(state['calls'], 6)
                self.assertEqual(state['baselines'][label], 'SCHEMA_FAILURE')
                folder = run / 'calls' / ('base-' + label)
                response = fixture.load(folder / 'a00/response.json')
                self.assertEqual(response['status'], 'SCHEMA_FAILURE')
                self.assertNotIn('result', response)
                self.assertFalse((folder / 'a01').exists())
                for name in ('RUN.md', 'BASELINE.md'):
                    report = fixture.read(run / name)
                    self.assertIn(label, report)
                    self.assertIn('SCHEMA_FAILURE', report)
                self.assertTrue((run / 'calls/c0001-use/a00/response.json').exists())

    def test_two_cycle_smoke_reports_exact_resource_envelope_and_baseline_settings(self):
        run = self.new_run(recipe='cross-family', cycles=2, baseline=True)
        state = engine.execute(run)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['completed_cycles'], 2)
        self.assertEqual(state['calls'], 11)
        self.assertEqual(state['baselines'], {'bare': 'COMPLETE', 'native': 'COMPLETE'})
        report = fixture.read(run / 'RUN.md')
        for expected in (
                'planned logical calls without early stop: 12.',
                'Completion allowance without repair/retry/fallback: 221184.',
                'Maximum attempts including repairs, fallbacks and configured transport retries: 28;',
                'maximum completion allowance: 573440.',
                'Native-to-off ceiling fallback calls: 0; allowance: 4.',
                'Baseline outcomes: `' + json.dumps({'bare': 'COMPLETE', 'native': 'COMPLETE'}, sort_keys=True) + '`.'):
            self.assertIn(expected, report)
        baseline = fixture.read(run / 'BASELINE.md')
        for label, thinking, cap in (('bare', 'off', 8192), ('native', 'native', 32768)):
            section = baseline.split('## ' + label + '\n\n', 1)[1].split('## ', 1)[0]
            self.assertIn('Outcome: `COMPLETE`.', section)
            self.assertIn('Thinking: ' + thinking + '; completion ceiling: ' + str(cap) +
                          '; declared reasoning effort: medium.', section)
        requests = sorted((run / 'calls').glob('*/a*/request.json'))
        self.assertEqual(len(requests), 11)
        for path in requests:
            request = fixture.load(path)
            self.assertEqual(request['prepared']['kwargs']['max_tokens'],
                             32768 if request['thinking'] == 'native' else 8192)
            self.assertEqual(request['prepared']['kwargs']['reasoning_effort'], 'medium')


if __name__ == '__main__':
    unittest.main()
