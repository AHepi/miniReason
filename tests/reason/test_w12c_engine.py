"""Offline optional-seat failures; retained evidence under work/review12b/tests."""
from tests.reason import artifact_root
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

EVIDENCE = artifact_root() / 'tests/e'
FAILURES = ('CEILING_HIT', 'TRANSPORT_OR_RESPONSE_ERROR', 'SCHEMA_FAILURE')


def quiet_reply(role, cycle, objections):
    if role == 'critic':
        return {'objections': []}
    return fixture.scripted_reply(role, cycle, objections)


class OptionalSeatEngineTests(unittest.TestCase):
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
        options = {'problem': 'Preserve the stated invariant at its boundary.',
                   'cycles': 1, 'recipe': 'cross-family', 'out': self.case / 'r',
                   'mode': 'offline'}
        options.update(kwargs)
        return engine.create_run(**options)

    def records(self, run):
        return {str(path.relative_to(run)): fixture.read(path)
                for path in (run / 'calls').rglob('*') if path.is_file()}

    @contextlib.contextmanager
    def failures(self, by_call):
        original = engine.Adapter.call
        def inject(adapter, **kwargs):
            failure = by_call.get(kwargs['coordinate']['call_id'])
            if failure == 'CEILING_HIT':
                kwargs['scripted'] = {'content': '', 'finish_reason': 'length',
                    'usage': {'prompt_tokens': 9, 'completion_tokens': kwargs['max_tokens'],
                              'total_tokens': 9 + kwargs['max_tokens']}}
            elif failure == 'SCHEMA_FAILURE':
                kwargs['scripted'] = {'content': 'Offline invalid public object.'}
            elif failure is not None:
                raise ReasonFailure(failure, 'Offline optional-seat failure fixture')
            return original(adapter, **kwargs)
        with mock.patch.object(engine.Adapter, 'call', inject):
            yield

    def assert_unavailable(self, run, role, code, cycle=1):
        phrase = role + ' unavailable: ' + code
        for path in (run / 'TRACE.md', run / 'cycles' / f'c{cycle:04d}' / 'CYCLE.md'):
            self.assertIn(phrase, fixture.read(path), str(path))

    def assert_record_preserved(self, run, saved):
        for relative, content in saved.items():
            self.assertEqual(fixture.read(run / relative), content, relative)

    def test_each_critic_failure_continues_with_parsed_peer_and_resumes_without_replay(self):
        for code in FAILURES:
            with self.subTest(code=code):
                run = self.new_run(out=self.case / code[:3])
                with self.failures({'c0001-k01': code}):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'cycle_budget')
                self.assertEqual(state['completed_cycles'], 1)
                self.assertEqual(fixture.load(run / 'config.json')['resilience_policy'],
                                 'reasoning-exposure-v2')
                self.assert_unavailable(run, 'critic', code)
                self.assertIn('Unavailable critic seats: 1', fixture.read(run / 'RUN.md'))
                self.assertTrue((run / 'calls/c0001-use/a00/response.json').exists())
                self.assertTrue(any(obj['id'].startswith('c0001-k02') for obj in state['objections']))
                self.assertFalse(any(obj['id'].startswith('c0001-k01') for obj in state['objections']))
                attempts = sorted((run / 'calls/c0001-k01').glob('a*/response.json'))
                self.assertEqual(len(attempts), 2 if code == 'SCHEMA_FAILURE' else 1)
                self.assertEqual(fixture.load(attempts[-1])['status'], code)
                saved, count = self.records(run), self.counter.offline
                resumed = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(resumed['stop_reason'], 'cycle_budget')
                self.assertEqual(self.counter.offline, count)
                self.assertEqual(self.records(run), saved)
                self.assert_unavailable(run, 'critic', code)

    def test_all_critics_unavailable_stops_with_last_failure_code(self):
        run = self.new_run()
        with self.failures({'c0001-k01': 'CEILING_HIT', 'c0001-k02': 'SCHEMA_FAILURE'}):
            state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'SCHEMA_FAILURE')
        self.assertEqual(state['completed_cycles'], 0)
        self.assertEqual(state['calls'], 4)
        self.assertFalse((run / 'calls/c0001-return').exists())
        self.assertFalse((run / 'calls/c0001-use').exists())
        for code in ('CEILING_HIT', 'SCHEMA_FAILURE'):
            self.assert_unavailable(run, 'critic', code)
        self.assertIn('Unavailable critic seats: 2', fixture.read(run / 'RUN.md'))

    def test_each_use_failure_completes_cycle_without_invented_objections(self):
        for code in FAILURES:
            with self.subTest(code=code):
                run = self.new_run(out=self.case / code[:3])
                with self.failures({'c0001-use': code}):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'cycle_budget')
                self.assertEqual(state['completed_cycles'], 1)
                self.assert_unavailable(run, 'use', code)
                self.assertIn('Unavailable use seats: 1', fixture.read(run / 'RUN.md'))
                self.assertFalse(any(obj['id'].startswith('c0001-use') for obj in state['objections']))
                attempts = sorted((run / 'calls/c0001-use').glob('a*/response.json'))
                self.assertEqual(len(attempts), 2 if code == 'SCHEMA_FAILURE' else 1)
                self.assertEqual(fixture.load(attempts[-1])['status'], code)

    def test_unavailable_critic_does_not_count_as_returned_empty_list(self):
        run = self.new_run(cycles=2)
        with self.failures({'c0001-k01': 'CEILING_HIT'}):
            state = engine.execute(run, scripted=quiet_reply)
        self.assertEqual(state['stop_reason'], 'no_new_objections')
        self.assertEqual(state['completed_cycles'], 2)
        self.assertEqual(state['calls'], 9)
        self.assertEqual(state['objections'], [])
        self.assert_unavailable(run, 'critic', 'CEILING_HIT')
        self.assertTrue((run / 'calls/c0002-use/a00/response.json').exists())

    def test_unavailable_use_does_not_count_as_returned_empty_list(self):
        run = self.new_run(cycles=2)
        with self.failures({'c0001-use': 'TRANSPORT_OR_RESPONSE_ERROR'}):
            state = engine.execute(run, scripted=quiet_reply)
        self.assertEqual(state['stop_reason'], 'no_new_objections')
        self.assertEqual(state['completed_cycles'], 2)
        self.assertEqual(state['calls'], 9)
        self.assertEqual(state['objections'], [])
        self.assert_unavailable(run, 'use', 'TRANSPORT_OR_RESPONSE_ERROR')

    def test_exhausted_native_fallback_is_optional_for_critic_and_use(self):
        recipe = copy.deepcopy(config.load_recipe('single-family')['data'])
        recipe['seats']['critics'].append(copy.deepcopy(recipe['seats']['critics'][0]))
        source = self.case / 'native.json'
        fixture.write(source, json.dumps(recipe, indent=2) + '\n')
        for role, cid in (('critic', 'c0001-k01'), ('use', 'c0001-use')):
            with self.subTest(role=role):
                run = self.new_run(recipe=source, out=self.case / role, retry_transport=2)
                with self.failures({cid: 'CEILING_HIT'}):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'cycle_budget')
                self.assertEqual(state['completed_cycles'], 1)
                self.assertEqual(state['calls'], 6)
                self.assert_unavailable(run, role, 'CEILING_HIT')
                first = fixture.load(run / 'calls' / cid / 'a00/request.json')
                second = fixture.load(run / 'calls' / cid / 'a01/request.json')
                self.assertEqual(first['thinking'], 'native')
                self.assertEqual(second['thinking'], 'off')
                self.assertTrue(second['ceiling_fallback'])
                self.assertEqual(first['prepared']['messages'], second['prepared']['messages'])
                self.assertFalse((run / 'calls' / cid / 'a02').exists())

    def test_other_failure_codes_remain_fatal_for_optional_seats(self):
        for role, cid in (('critic', 'c0001-k01'), ('use', 'c0001-use')):
            with self.subTest(role=role):
                run = self.new_run(out=self.case / role)
                with self.failures({cid: 'INCOMPLETE_GENERATION'}):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'INCOMPLETE_GENERATION')
                self.assertEqual(state['completed_cycles'], 0)
                self.assertNotIn(role + ' unavailable:', fixture.read(run / 'TRACE.md'))
                if role == 'critic':
                    self.assertFalse((run / 'calls/c0001-k02').exists())

    def test_conjecture_and_return_remain_fatal_after_exhausted_fallback(self):
        for role, cid in (('conjecture', 'initial'), ('return', 'c0001-return')):
            with self.subTest(role=role):
                run = self.new_run(out=self.case / role)
                with self.failures({cid: 'CEILING_HIT'}):
                    state = engine.execute(run, scripted=fixture.scripted_reply)
                self.assertEqual(state['stop_reason'], 'CEILING_HIT')
                self.assertEqual(state['completed_cycles'], 0)
                self.assertTrue((run / 'calls' / cid / 'a01/response.json').exists())
                self.assertFalse((run / 'calls' / cid / 'a02').exists())
                self.assertFalse((run / 'calls/c0001-use').exists())

    def test_interrupted_critic_failure_recovers_without_replaying_failed_attempt(self):
        class Interrupted(BaseException):
            pass
        def interrupt(cid, response):
            if cid == 'c0001-k01':
                raise Interrupted()
        run = self.new_run()
        with self.failures({'c0001-k01': 'CEILING_HIT'}):
            with self.assertRaises(Interrupted):
                engine.execute(run, scripted=fixture.scripted_reply, after_call=interrupt)
        saved, before = self.records(run), self.counter.offline
        self.assertEqual(before, 2)
        state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(self.counter.offline - before, 3)
        self.assert_record_preserved(run, saved)
        self.assert_unavailable(run, 'critic', 'CEILING_HIT')
        self.assertFalse((run / 'calls/c0001-k01/a01').exists())

    def test_saved_v1_policy_keeps_gateway_ceiling_and_fatal_critic(self):
        recipe = copy.deepcopy(config.load_recipe('cross-family')['data'])
        seats = [recipe['seats']['use'], *recipe['seats']['critics']]
        for seat in seats:
            seat['endpoint'] = seat['endpoint'].removesuffix('.native')
            seat['thinking'] = 'gateway-default'
        recipe['lineages'] = {config.seat_name(seat): config.lineage(seat)
                             for seat in [recipe['seats']['conjecture'], *seats]}
        source = self.case / 'v1.json'
        fixture.write(source, json.dumps(recipe, indent=2) + '\n')
        run = self.new_run(recipe=source)
        cfg = fixture.load(run / 'config.json')
        cfg['resilience_policy'] = 'native-off-v1'
        fixture.write(run / 'config.json', json.dumps(cfg, indent=2) + '\n')
        frozen = {name: fixture.read(run / name) for name in ('config.json', 'recipe.json')}
        with self.failures({'c0001-k01': 'CEILING_HIT'}):
            state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'CEILING_HIT')
        self.assertEqual(state['completed_cycles'], 0)
        request = fixture.load(run / 'calls/c0001-k01/a00/request.json')
        self.assertEqual(request['thinking'], 'gateway-default')
        self.assertEqual(request['prepared']['kwargs']['max_tokens'], 8192)
        self.assertFalse((run / 'calls/c0001-k02').exists())
        self.assertNotIn('critic unavailable:', fixture.read(run / 'TRACE.md'))
        saved, before = self.records(run), self.counter.offline
        resumed = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(resumed['stop_reason'], 'CEILING_HIT')
        self.assertEqual(self.counter.offline, before)
        self.assertEqual(self.records(run), saved)
        for name, text in frozen.items():
            self.assertEqual(fixture.read(run / name), text)

    def test_ollama_native_ceiling_fallback_uses_existing_think_field(self):
        recipe = copy.deepcopy(config.load_recipe('cross-family')['data'])
        recipe['seats']['critics'][0] = {
            'endpoint': 'ollama/qwen3.5-397b.native', 'thinking': 'native',
            'reasoning_effort': 'medium'}
        seats = [recipe['seats']['conjecture'], recipe['seats']['use'],
                 *recipe['seats']['critics']]
        recipe['lineages'] = {config.seat_name(seat): config.lineage(seat) for seat in seats}
        source = self.case / 'ollama.json'
        fixture.write(source, json.dumps(recipe, indent=2) + '\n')
        run = self.new_run(recipe=source)
        original = engine.Adapter.call
        def length_once(adapter, **kwargs):
            coordinate = kwargs['coordinate']
            if coordinate['call_id'] == 'c0001-k01' and coordinate['attempt'] == 0:
                kwargs['scripted'] = {'content': '', 'finish_reason': 'length',
                    'usage': {'prompt_tokens': 9, 'completion_tokens': 32768,
                              'total_tokens': 32777}}
            return original(adapter, **kwargs)
        with mock.patch.object(engine.Adapter, 'call', length_once):
            state = engine.execute(run, scripted=fixture.scripted_reply)
        self.assertEqual(state['stop_reason'], 'cycle_budget')
        self.assertEqual(state['completed_cycles'], 1)
        self.assertEqual(state['calls'], 6)
        first = fixture.load(run / 'calls/c0001-k01/a00/request.json')
        second = fixture.load(run / 'calls/c0001-k01/a01/request.json')
        self.assertEqual(first['thinking'], 'native')
        self.assertEqual(second['thinking'], 'off')
        self.assertTrue(second['ceiling_fallback'])
        self.assertEqual(first['prepared']['messages'], second['prepared']['messages'])
        for attempt, request, thinking in (('a00', first, True), ('a01', second, False)):
            self.assertEqual(request['prepared']['kwargs']['max_tokens'], 32768)
            self.assertEqual(request['prepared']['kwargs']['extra'], {'think': thinking})
            self.assertIs(request['prepared']['payload']['think'], thinking)
            wire = fixture.load(run / 'calls/c0001-k01' / attempt / 'provider/call-0001.request.json')
            payload = json.loads(wire['wire_body_text'])
            self.assertEqual(payload, request['prepared']['payload'])
            self.assertIs(payload['think'], thinking)
            self.assertEqual(payload['options']['num_predict'], 32768)
        self.assertFalse((run / 'calls/c0001-k01/a02').exists())
        self.assertNotIn('critic unavailable:', fixture.read(run / 'TRACE.md'))


if __name__ == '__main__':
    unittest.main()
