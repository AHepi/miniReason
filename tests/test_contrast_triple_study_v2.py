"""Offline tests for C001 under the SUCCESSOR driver. No live call, no credential read.

This file is the v1 suite `tests/test_contrast_triple_study.py` re-pointed at
`tools/contrast_triple_study_v2.py`, plus the classes at the end of the file that test
what v2 adds. Every inherited test runs against the PUBLISHED occurrence-01 material,
unchanged, which is the parity claim: on a material that declares no `dispatch_scope`,
v2 does what v1 does.

The provider transport is exercised only through `OfflineProvider` (preflight) and a
scripted stand-in that writes the same write-once call records the live provider writes.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import re
import sys
import threading
import time
import unittest
from pathlib import Path

STAGE = Path(__file__).resolve().parents[1]
REPO = Path(os.environ.get('MINIREASON_REPO', '/home/user/miniReason'))
# The transport is resolved from MINIREASON_PROVIDER_SRC when the operator sets it and
# otherwise from the repository's own `src`, where the module lives after publication.
# No session-specific staging path is baked in, and this file never exports a provider
# path into the environment: a stale default would silently shadow the published module,
# which is the one thing the suite exists to rule out.
PROVIDER_SRC = os.environ.get('MINIREASON_PROVIDER_SRC') or str(REPO / 'src')
# `REPO / 'tools'` is where the PUBLISHED v1 driver lives, and this suite imports it to
# prove the parity claim. After publication STAGE is REPO and the two entries are one.
for entry in (str(STAGE / 'tools'), str(REPO / 'tools'), str(REPO / 'src'), PROVIDER_SRC):
    while entry in sys.path:
        sys.path.remove(entry)
    sys.path.insert(0, entry)

import contrast_triple_study_v2 as c  # noqa: E402
import contrast_triple_study as v1  # noqa: E402

MATERIAL = STAGE / 'experiments/diagnostics/C001-contrast-triple/material.json'
if not MATERIAL.exists():
    # Staging layout only: before publication this file sits beside the successor driver
    # rather than in the repository's own tests/, so STAGE is the staging directory. After
    # publication STAGE is the repository and the first path is the one that exists.
    MATERIAL = REPO / 'experiments/diagnostics/C001-contrast-triple/material.json'
# The occurrence-02 material: same study, one cell, the raised ceiling and timeout.
MATERIAL_V2 = MATERIAL.parent / 'material-occurrence-02.json'
if not MATERIAL_V2.exists():
    MATERIAL_V2 = STAGE / 'material.json'
V1_SOURCE = Path(v1.__file__)
V2_SOURCE = Path(c.__file__)
# The register directory: PLAN.md, NOTES.md and RECODING_TABLE.md live beside the
# material, in the staging layout and in the published one alike.
REGISTER = MATERIAL.parent
H005 = REPO / 'experiments/diagnostics/H005-open-prose-commitments'


def material_v2() -> dict:
    return c.validate_material(json.loads(MATERIAL_V2.read_bytes()))


def material() -> dict:
    return c.validate_material(json.loads(MATERIAL.read_bytes()))


# ----------------------------------------------------------------- scripted provider

class ScriptedProvider:
    """Same call surface and same record files as OpenAICompatProvider, no socket.

    `plan` maps a coordinate label to the reply it returns. It is a routing fixture:
    the text it returns is never read as a semantic result by any test.
    """

    observed: dict[str, int] = {}
    peak: dict[str, int] = {}
    _lock = threading.Lock()
    replies: dict = {}
    hold_seconds = 0.0

    def __init__(self, endpoint: dict, records: Path):
        self.endpoint = endpoint
        self.records = Path(records)

    @classmethod
    def reset(cls, replies=None, hold_seconds: float = 0.0) -> None:
        cls.observed, cls.peak = {}, {}
        cls.replies = replies or {}
        cls.hold_seconds = hold_seconds

    def complete(self, messages, *, response_format=None, max_tokens=8192,
                 temperature=None, seed=None, extra=None, coordinate=None):
        key = self.endpoint['key_env']
        with ScriptedProvider._lock:
            ScriptedProvider.observed[key] = ScriptedProvider.observed.get(key, 0) + 1
            ScriptedProvider.peak[key] = max(ScriptedProvider.peak.get(key, 0),
                                             ScriptedProvider.observed[key])
        try:
            if ScriptedProvider.hold_seconds:
                time.sleep(ScriptedProvider.hold_seconds)
            payload = {'model': self.endpoint['model'], 'messages': [dict(m) for m in messages],
                       'stream': False, 'max_tokens': max_tokens,
                       'response_format': dict(response_format)}
            if seed is not None:
                payload['seed'] = seed
            label = '{}/{}/{}/rep{}'.format(coordinate['endpoint_slug'], coordinate['arm'],
                                            coordinate['case'], coordinate['replicate'])
            reply = ScriptedProvider.replies.get(
                label, {'content': json.dumps({'body': 'offline routing sentinel ' + label,
                                               'commitments': ''})})
            record = {'schema_version': 'minireason.call.v2', 'call_number': 1,
                      'request': payload, 'request_sha256': c.digest(payload),
                      'coordinate': dict(coordinate or {}),
                      'status': reply.get('status', 'COMPLETE'),
                      'finish_reason': reply.get('finish_reason', 'stop'),
                      'content': reply['content'],
                      'usage': reply.get('usage', {'prompt_tokens': 11, 'completion_tokens': 7,
                                                   'total_tokens': 18}),
                      'returned_model': self.endpoint['model'],
                      'reasoning_content_present': reply.get('reasoning_content_present', False),
                      'reasoning_content_persisted': False, 'credential_redaction': False}
            c.write_new(self.records / 'call-0001.request.json',
                        {k: record[k] for k in ('schema_version', 'request', 'request_sha256',
                                                'coordinate')})
            c.write_new(self.records / 'call-0001.response.json', record)
            return record
        finally:
            with ScriptedProvider._lock:
                ScriptedProvider.observed[key] -= 1


def prepared(tmp: Path) -> tuple[Path, dict]:
    out = tmp / 'occ'
    result = c.prepare(MATERIAL, out, REPO)
    return out, result


# ----------------------------------------------------------------- material integrity

class MaterialIntegrity(unittest.TestCase):

    def test_source_pins_match_the_real_occurrence_files(self):
        checked = c.check_material_integrity(material(), REPO)
        for name, value in checked.items():
            self.assertEqual(hashlib.sha256((REPO / name).read_bytes()).hexdigest(), value)
        self.assertIn('docs/sources/FW5-explanatory-construction.md', checked)
        self.assertEqual(
            checked['docs/sources/FW5-explanatory-construction.md'],
            '8105925b07db4a17f15c38cbad79aaca16653d94b0503de79756b5ece33ee63a')

    def test_original_case_is_the_occurrence_bytes(self):
        data = material()
        for arm, source in (('fcl', 'mini_fcl'), ('prose', 'mini_prose')):
            artifact = json.loads(
                (H005 / f'occurrence-01/artifacts/daily/{source}/cycle01/objection.json').read_bytes())
            case = data['arms'][arm]['cases']['original']
            self.assertEqual(case['body'], artifact['body'])
            self.assertEqual(case['commitments'], artifact['commitments'])

    def test_frozen_projections_are_what_the_h005_response_node_saw(self):
        data = material()
        for arm, source in (('fcl', 'mini_fcl'), ('prose', 'mini_prose')):
            request = json.loads(
                (H005 / f'occurrence-01/requests/daily/{source}/cycle01/response.json').read_bytes())
            brief = request['messages'][1]['content']
            block = data['arms'][arm]
            self.assertIn(block['cases']['original']['objection_projection'], brief)
            for name in ('account', 'rival'):
                self.assertIn(block['frozen_inputs'][name]['projection'], brief)

    def test_node_instruction_is_verbatim_from_h005_material(self):
        data = material()
        h005 = json.loads((H005 / 'material.json').read_bytes())
        node = next(n for n in h005['templates']['fork5']['nodes'] if n['id'] == 'response')
        self.assertEqual(data['node']['instruction'], node['instruction'])
        self.assertEqual(data['system_common'], h005['system'])
        self.assertEqual(data['policies']['fcl'], h005['formal_instruction'])
        self.assertEqual(data['policies']['prose'], h005['prose_instruction'])

    def test_a_tampered_pin_is_refused(self):
        data = material()
        data['source_pins']['docs/sources/FW5-explanatory-construction.md'] = '0' * 64
        with self.assertRaises(ValueError):
            c.check_material_integrity(data, REPO)


# ----------------------------------------------------------------- recoding

class Recoding(unittest.TestCase):

    def test_every_original_unit_is_mapped_and_the_recoding_reconstructs(self):
        report = c.check_recoding(material())
        self.assertEqual(report['fcl']['units'], 50)
        self.assertEqual(report['prose']['units'], 35)
        for arm in ('fcl', 'prose'):
            self.assertTrue(report[arm]['every_original_unit_mapped'])
            self.assertTrue(report[arm]['recoded_document_reconstructible_from_table'])

    def test_a_dropped_unit_is_refused(self):
        data = material()
        data['arms']['prose']['recoding']['units'].pop()
        data['arms']['prose']['recoding']['unit_count'] -= 1
        with self.assertRaises(ValueError):
            c.check_recoding(data)

    def test_recoding_preserves_fcl_structure_and_changes_the_words(self):
        data = material()
        block = data['arms']['fcl']
        self.assertEqual(c.fcl_structure(block['cases']['original']['commitments']),
                         c.fcl_structure(block['cases']['recoding']['commitments']))
        self.assertNotEqual(block['cases']['original']['commitments'],
                            block['cases']['recoding']['commitments'])
        for arm in ('fcl', 'prose'):
            cases = data['arms'][arm]['cases']
            self.assertNotEqual(c.normalise_prose(cases['original']['body']),
                                c.normalise_prose(cases['recoding']['body']))

    def test_recoding_table_file_matches_the_material(self):
        rendered = c.render_recoding_table(material())
        staged = (REGISTER / 'RECODING_TABLE.md')
        self.assertEqual(staged.read_text(encoding='utf-8'), rendered)


# ----------------------------------------------------------------- carrier

class Carrier(unittest.TestCase):

    def test_carrier_normalises_to_identical_content_tokens(self):
        data = material()
        report = c.check_carrier(data)
        for arm in ('fcl', 'prose'):
            cases = data['arms'][arm]['cases']
            self.assertEqual(c.normalise_prose(cases['original']['body']),
                             c.normalise_prose(cases['carrier']['body']))
            self.assertNotEqual(cases['original']['body'], cases['carrier']['body'])
            self.assertTrue(report[arm]['content_tokens_identical'])
        fcl = data['arms']['fcl']['cases']
        self.assertEqual(c.canonical_fcl(fcl['original']['commitments']),
                         c.canonical_fcl(fcl['carrier']['commitments']))
        self.assertNotEqual(json.loads(fcl['original']['commitments'])['records'][0]['id'],
                            json.loads(fcl['carrier']['commitments'])['records'][0]['id'])
        prose = data['arms']['prose']['cases']
        self.assertEqual(c.normalise_prose(prose['original']['commitments']),
                         c.normalise_prose(prose['carrier']['commitments']))
        self.assertIn('\n- ', '\n' + prose['carrier']['commitments'])

    def test_a_content_change_smuggled_into_the_carrier_is_refused(self):
        data = material()
        data['arms']['prose']['cases']['carrier']['body'] += ' An extra sentence.'
        with self.assertRaises(ValueError):
            c.check_carrier(data)


# ----------------------------------------------------------------- control

class Control(unittest.TestCase):

    def test_control_carries_no_objection_content(self):
        report = c.check_control(material())
        for arm in ('fcl', 'prose'):
            self.assertEqual(report[arm]['objection_shingles_leaked'], 0)
            self.assertTrue(report[arm]['objection_block_is_the_runner_absent_wording'])

    def test_control_uses_the_runners_own_absent_wording(self):
        data = material()
        expected = 'Source objection: absent in the first template invocation; selected view both.'
        for arm in ('fcl', 'prose'):
            self.assertEqual(data['arms'][arm]['cases']['control']['objection_projection'], expected)

    def test_control_is_refused_if_objection_text_is_left_in(self):
        data = material()
        block = data['arms']['fcl']
        block['cases']['control']['objection_projection'] = block['cases']['original']['objection_projection']
        with self.assertRaises(ValueError):
            c.check_control(data)


# ----------------------------------------------------------------- single-node guarantee

class SingleNodeGuarantee(unittest.TestCase):
    """Appendix B item 14: the fork5 objection/rival pair differ in instruction as well as
    view, so a difference there cannot be attributed to the withheld content. C001 varies
    exactly one block of one node."""

    def test_only_the_objection_block_differs_between_cases(self):
        data = material()
        for arm in ('fcl', 'prose'):
            head, tail = c.shared_envelope(data, arm)
            for case in c.CASES:
                projection = data['arms'][arm]['cases'][case]['objection_projection']
                self.assertEqual(c.brief_for(data, arm, case), head + projection + tail)
            self.assertIn(data['node']['instruction'], head)
            self.assertIn(data['arms'][arm]['frozen_inputs']['account']['projection'], head)
            self.assertIn(data['arms'][arm]['frozen_inputs']['rival']['projection'], tail)

    def test_system_message_is_identical_across_cases(self):
        data = material()
        for arm in ('fcl', 'prose'):
            systems = {c.messages_for(data, arm, case)[0]['content'] for case in c.CASES}
            self.assertEqual(len(systems), 1)


# ----------------------------------------------------------------- preflight and plan

class Preflight(unittest.TestCase):

    def test_preflight_plans_240_calls_and_makes_none(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            self.assertEqual(result['planned_calls'], 240)
            self.assertEqual(result['provider_calls'], 0)
            preflight = json.loads((out / 'preflight.json').read_bytes())
            self.assertEqual(preflight['status'], 'OFFLINE_PREFLIGHT_PASSED')
            self.assertEqual(preflight['distinct_message_pairs'], 8)
            self.assertIn('OfflineProvider', preflight['offline_provider'])
            self.assertFalse((out / 'requests').exists())
            self.assertFalse((out / 'provider').exists())

    def test_plan_identity_is_deterministic_and_clock_free(self):
        import tempfile
        with tempfile.TemporaryDirectory() as one, tempfile.TemporaryDirectory() as two:
            first = c.prepare(MATERIAL, Path(one) / 'a', REPO)
            time.sleep(1.05)
            second = c.prepare(MATERIAL, Path(two) / 'b', REPO)
            self.assertEqual(first['plan_id'], second['plan_id'])
            self.assertEqual(
                (Path(one) / 'a' / 'plan.json').read_bytes(),
                (Path(two) / 'b' / 'plan.json').read_bytes())

    def test_plan_counts_and_ceilings(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
            self.assertEqual(len(plan['coordinates']), 240)
            self.assertEqual(len(plan['endpoints']), 6)
            self.assertEqual(plan['ceilings']['max_tokens'],
                             {'deepseek-flash': 8192,
                              'ollama/gpt-oss-120b': 32768,
                              'ollama/qwen3.5-397b': 32768,
                              'ollama/glm-5.3': 32768,
                              'ollama/kimi-k3': 32768,
                              'ollama/gemma4-31b': 32768})
            self.assertEqual(plan['ceilings']['max_tokens_authorised_maximum'], 32768)
            self.assertEqual(plan['ceilings']['timeout_seconds'],
                             {'deepseek-flash': 180,
                              'ollama/gpt-oss-120b': 600,
                              'ollama/qwen3.5-397b': 600,
                              'ollama/glm-5.3': 600,
                              'ollama/kimi-k3': 600,
                              'ollama/gemma4-31b': 600})
            self.assertEqual(plan['ceilings']['timeout_seconds_authorised_maximum'], 600)
            self.assertEqual(plan['ceilings']['automatic_retries'], 0)
            self.assertEqual(plan['ceilings']['max_concurrent_per_key'], 5)
            self.assertEqual(plan['ceilings']['temperature'], 'provider-default')
            self.assertEqual(len({c.label(x) for x in plan['coordinates']}), 240)

    def test_max_tokens_is_per_endpoint_and_reaches_every_payload(self):
        import tempfile
        data = material()
        caps = data['ceilings']['max_tokens']
        for endpoint in data['endpoints']:
            self.assertEqual(endpoint['max_tokens'], caps[endpoint['id']], endpoint['id'])
            self.assertEqual(endpoint['max_tokens'],
                             8192 if endpoint['id'] == 'deepseek-flash' else 32768)
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
        planned = {e['slug']: e['max_tokens'] for e in plan['endpoints']}
        seen = {}
        for coord in plan['coordinates']:
            endpoint = next(e for e in data['endpoints'] if e['slug'] == coord['endpoint_slug'])
            spec = c.spec_for(endpoint, coord)
            payload = c.payload_for(c.messages_for(data, coord['arm'], coord['case']), spec)
            self.assertEqual(payload['max_tokens'], planned[coord['endpoint_slug']],
                             c.label(coord))
            seen.setdefault(coord['endpoint_slug'], set()).add(payload['max_tokens'])
        self.assertEqual({k: sorted(v) for k, v in seen.items()},
                         {k: [v] for k, v in planned.items()})

    def test_the_raised_ceiling_is_inside_the_transports_own_validation_range(self):
        import tempfile
        endpoint = next(e for e in material()['endpoints'] if e['id'] == 'ollama/glm-5.3')
        with tempfile.TemporaryDirectory() as tmp:
            provider, _ = c._offline_provider(endpoint, Path(tmp))
            provider._validate_call_args(max_tokens=32768, reasoning_effort='high', extra=None)
            built = provider._build_payload(
                [{'role': 'user', 'content': 'return json'}],
                response_format={'type': 'json_object'}, max_tokens=32768,
                temperature=None, seed=1, thinking=None, reasoning_effort='high', extra=None)
            self.assertEqual(built['max_tokens'], 32768)
            self.assertNotIn('temperature', built)
            with self.assertRaises(ValueError):
                provider._validate_call_args(max_tokens=c.MAX_TOKENS_AUTHORISED * 100,
                                             reasoning_effort='high', extra=None)

    def test_a_material_whose_ceiling_table_and_endpoint_disagree_is_refused(self):
        data = json.loads(MATERIAL.read_bytes())
        data['endpoints'][1]['max_tokens'] = 8192
        with self.assertRaises(ValueError) as caught:
            c.validate_material(data)
        self.assertEqual(str(caught.exception), 'MATERIAL_ENDPOINT_MAX_TOKENS')
        over = json.loads(MATERIAL.read_bytes())
        over['endpoints'][1]['max_tokens'] = 65536
        over['ceilings']['max_tokens'][over['endpoints'][1]['id']] = 65536
        with self.assertRaises(ValueError) as caught:
            c.validate_material(over)
        self.assertEqual(str(caught.exception), 'MATERIAL_ENDPOINT_MAX_TOKENS')

    def test_a_payload_built_with_another_endpoints_ceiling_is_refused(self):
        import tempfile
        data = material()
        plan = c.plan_body(data, MATERIAL.read_bytes(), b'helper')
        plan['plan_id'] = c.digest(plan)
        original = c.payload_for

        def wrong(messages, spec):
            payload = original(messages, spec)
            payload['max_tokens'] = 8192 if payload['max_tokens'] != 8192 else 32768
            return payload

        c.payload_for = wrong
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError) as caught:
                    c._offline_preflight(data, plan, None, Path(tmp))
            self.assertEqual(str(caught.exception), 'CEILING_NOT_APPLIED')
        finally:
            c.payload_for = original

    def test_every_planned_endpoint_resolves_in_the_registry(self):
        for endpoint in material()['endpoints']:
            resolved = c.resolve_endpoint(endpoint)
            self.assertEqual(resolved.model, endpoint['model'])
            self.assertEqual(resolved.key_env, endpoint['key_env'])
            self.assertFalse(resolved.native)
            self.assertLessEqual(resolved.max_concurrency, 5)
            self.assertEqual(resolved.timeout_seconds, endpoint['timeout_seconds'])


# ----------------------------------------------------------------- write-once and replay

class Custody(unittest.TestCase):

    def test_write_new_refuses_a_second_write(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'x.json'
            c.write_new(path, {'a': 1})
            with self.assertRaises(FileExistsError):
                c.write_new(path, {'a': 2})

    def test_prepare_refuses_to_overwrite_an_occurrence(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            with self.assertRaises(FileExistsError):
                c.prepare(MATERIAL, out, REPO)

    def test_no_replay(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset()
            only = (lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                    and coord['arm'] == 'fcl' and coord['replicate'] == 1)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None, only=only)
            with self.assertRaises(FileExistsError):
                c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                      notify=lambda _: None, only=only)

    def test_run_refuses_a_foreign_plan_id(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            with self.assertRaises(ValueError):
                c.run(out, '0' * 64, REPO, provider_factory=ScriptedProvider,
                      notify=lambda _: None, only=lambda coord: False)


# ----------------------------------------------------------------- concurrency

class Concurrency(unittest.TestCase):

    def test_key_gate_admits_at_most_five(self):
        gate, live, peak, lock = c.KeyGate(), 0, 0, threading.Lock()

        def worker():
            nonlocal live, peak
            with gate.slot('OLLAMA_API_KEY'):
                with lock:
                    live += 1
                    peak = max(peak, live)
                time.sleep(0.02)
                with lock:
                    live -= 1

        threads = [threading.Thread(target=worker) for _ in range(24)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertLessEqual(peak, 5)

    def test_no_wave_exceeds_five_per_key(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
            key_env = {e['slug']: e['key_env'] for e in plan['endpoints']}
            total = 0
            for wave in c.build_waves(plan):
                counts = {}
                for coord in wave['coordinates']:
                    key = key_env[coord['endpoint_slug']]
                    counts[key] = counts.get(key, 0) + 1
                self.assertTrue(all(n <= 5 for n in counts.values()))
                total += len(wave['coordinates'])
            self.assertEqual(total, 240)

    def test_dispatch_never_exceeds_five_in_flight_per_key(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset(hold_seconds=0.01)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['endpoint_slug'] in ('deepseek-flash',
                                                                'ollama-gpt-oss-120b'))
            for key, peak in ScriptedProvider.peak.items():
                self.assertLessEqual(peak, 5, key)


# ----------------------------------------------------------------- decoding

class Decoding(unittest.TestCase):

    def _spec(self):
        return c.spec_for(material()['endpoints'][0],
                          c.coordinate('deepseek-flash', 'fcl', 'original', 1))

    def _record(self, content, **over):
        payload = {'model': 'deepseek-flash', 'messages': [], 'stream': False,
                   'max_tokens': 8192, 'response_format': {'type': 'json_object'}, 'seed': 1}
        record = {'request': payload, 'request_sha256': c.digest(payload), 'content': content,
                  'usage': {'prompt_tokens': 3, 'completion_tokens': 4}, 'status': 'COMPLETE',
                  'finish_reason': 'stop', 'reasoning_content_persisted': False,
                  'credential_redaction': False, 'returned_model': 'deepseek-flash'}
        record.update(over)
        return record, payload

    def test_clean_envelope_needs_no_repair(self):
        record, payload = self._record(json.dumps({'body': 'b', 'commitments': 'k'}))
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['envelope_status'], 'AUTHORED')
        self.assertEqual(out['envelope_repairs'], [])
        self.assertTrue(out['strict_parse_would_succeed'])
        self.assertTrue(out['comparable'])

    def test_a_single_code_fence_is_stripped_and_recorded(self):
        inner = json.dumps({'body': 'b', 'commitments': 'k'})
        record, payload = self._record('```json\n' + inner + '\n```')
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['envelope_status'], 'AUTHORED')
        self.assertEqual(out['envelope_repairs'], ['strip_outer_code_fence'])
        self.assertFalse(out['strict_parse_would_succeed'])
        self.assertEqual(out['body'], 'b')

    def test_control_characters_admitted_only_under_the_declared_relaxation(self):
        raw = '{"body": "line\tbreak", "commitments": "k"}'
        record, payload = self._record(raw)
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['envelope_repairs'], ['json_strict_false'])
        self.assertFalse(out['strict_parse_would_succeed'])

    def test_unrepairable_text_stays_opaque_and_is_not_rewritten(self):
        record, payload = self._record('I will not return JSON.')
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['envelope_status'], 'OPAQUE')
        self.assertEqual(out['body'], 'I will not return JSON.')
        self.assertEqual(out['commitments'], '')

    def test_partial_delivery_is_unresolved(self):
        record, payload = self._record('{"body": "trunc',
                                       status='INCOMPLETE_GENERATION', finish_reason='length')
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['delivery_status'], 'PARTIAL')
        self.assertFalse(out['comparable'])
        self.assertIn('unresolved', out['unresolved_reason'])

    def test_missing_usage_is_unknown_not_zero(self):
        record, payload = self._record(json.dumps({'body': 'b', 'commitments': 'k'}), usage={})
        out = c.decode_contribution(record, payload, self._spec())
        self.assertEqual(out['usage_status'], 'UNKNOWN')
        self.assertIsNone(out['usage'])

    def test_a_foreign_payload_is_a_custody_failure(self):
        record, payload = self._record(json.dumps({'body': 'b', 'commitments': 'k'}))
        record['request'] = {'model': 'somewhere-else'}
        with self.assertRaises(ValueError):
            c.decode_contribution(record, payload, self._spec())

    def test_persisted_reasoning_text_is_a_custody_failure(self):
        record, payload = self._record(json.dumps({'body': 'b', 'commitments': 'k'}),
                                       reasoning_content_persisted=True)
        with self.assertRaises(ValueError):
            c.decode_contribution(record, payload, self._spec())


# ----------------------------------------------------------------- table

class Comparison(unittest.TestCase):

    @staticmethod
    def _replies():
        fcl = json.dumps({'body': 'b',
                          'commitments': json.dumps({'language': 'FCL-1', 'records': [
                              {'id': 'k1', 'type': 'use', 'text': 't',
                               'target': ['objection#o1']}],
                              'uptake': ['k1']})})
        out = {}
        for case in c.CASES:
            for rep in range(1, 6):
                out[f'deepseek-flash/fcl/{case}/rep{rep}'] = {'content': fcl}
                out[f'deepseek-flash/prose/{case}/rep{rep}'] = {
                    'content': json.dumps({'body': 'b', 'commitments': 'k'})}
        out['deepseek-flash/fcl/original/rep5'] = {
            'content': '{"body": "cut off', 'status': 'INCOMPLETE_GENERATION',
            'finish_reason': 'length'}
        return out

    def _run_and_table(self, tmp: Path):
        out, result = prepared(tmp)
        ScriptedProvider.reset(replies=self._replies())
        c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
              notify=lambda _: None,
              only=lambda coord: coord['endpoint_slug'] == 'deepseek-flash')
        return out, c.table(out, REPO, force=True)

    def test_table_has_empty_root_columns_and_no_scoring_keys(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            data = json.loads((out / 'comparison.json').read_bytes())
            c.assert_no_scoring_keys(data)
            self.assertTrue(data['tables'])
            for entry in data['tables']:
                self.assertEqual(set(entry['root_reading']), set(c.EMPTY_ROOT_COLUMNS))
                self.assertTrue(all(v == '' for v in entry['root_reading'].values()))
            rendered = (out / 'COMPARISON.md').read_text(encoding='utf-8')
            for column in c.EMPTY_ROOT_COLUMNS:
                self.assertIn(column, rendered)
            headers = {cell.strip().lower()
                       for line in rendered.splitlines() if line.startswith('|')
                       for cell in line.strip('|').split('|')}
            self.assertFalse(headers & c.FORBIDDEN_KEYS, headers & c.FORBIDDEN_KEYS)

    def test_mechanical_columns_are_present_for_fcl_and_withheld_for_prose(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            data = json.loads((out / 'comparison.json').read_bytes())
            fcl = next(t for t in data['tables'] if t['arm'] == 'fcl')
            prose = next(t for t in data['tables'] if t['arm'] == 'prose')
            row = fcl['cases']['original'][0]
            self.assertEqual(row['fcl']['parse'], 'OK')
            self.assertEqual(row['fcl']['records_by_type']['use'], 1)
            self.assertEqual(row['fcl']['objection_record_ids_in_refs'], ['o1'])
            self.assertEqual(row['fcl']['uptake'], ['k1'])
            self.assertEqual(prose['cases']['original'][0]['mechanical'],
                             'none beyond byte hashes and lengths')
            self.assertNotIn('fcl', prose['cases']['original'][0])

    def test_a_partial_cell_is_unresolved_and_not_compared(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            data = json.loads((out / 'comparison.json').read_bytes())
            fcl = next(t for t in data['tables'] if t['arm'] == 'fcl')
            row = next(r for r in fcl['cases']['original'] if r['replicate'] == 5)
            self.assertEqual(row['delivery_status'], 'PARTIAL')
            self.assertFalse(row['comparable'])
            self.assertNotIn('fcl', row)
            self.assertEqual(row['mechanical'], 'withheld: cell unresolved')
            self.assertIn('original/rep5', fcl['unresolved_cells'])

    def test_audit_recomputes_custody_over_written_coordinates(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            report = c.audit(out, REPO)
            self.assertEqual(report['planned_calls'], 240)
            self.assertEqual(report['counts']['not_dispatched'], 200)
            self.assertEqual(report['counts']['COMPLETE'], 39)
            self.assertEqual(report['counts']['PARTIAL'], 1)
            self.assertEqual(report['counts']['unresolved_partial'], 1)
            self.assertEqual(report['counts']['unresolved_attempts'], 0)

    def test_tampering_with_a_delivered_byte_is_caught(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            coord = c.coordinate('deepseek-flash', 'fcl', 'control', 1)
            path = c.provider_dir(out, coord) / 'call-0001.response.json'
            path.write_bytes(path.read_bytes().replace(b'"call_number": 1',
                                                        b'"call_number": 2'))
            with self.assertRaises(ValueError):
                c.audit(out, REPO)

    def test_record_layout_is_the_declared_one(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            for name in ('requests/deepseek-flash/fcl/original/rep1.json',
                         'attempts/deepseek-flash/fcl/original/rep1.json',
                         'responses/deepseek-flash/fcl/original/rep1.json',
                         'responses/deepseek-flash/fcl/original/rep1.txt',
                         'artifacts/deepseek-flash/fcl/original/rep1.json',
                         'provider/deepseek-flash/fcl/original/rep1/call-0001.request.json',
                         'provider/deepseek-flash/fcl/original/rep1/call-0001.response.json',
                         'juxtaposition/deepseek-flash__fcl.md'):
                self.assertTrue((out / name).exists(), name)

    def test_requests_differ_only_in_the_objection_block(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = self._run_and_table(Path(tmp))
            data = material()
            briefs = {}
            for case in c.CASES:
                request = json.loads(
                    (out / f'requests/deepseek-flash/fcl/{case}/rep1.json').read_bytes())
                briefs[case] = request['messages'][1]['content']
                self.assertEqual(request['messages'][0]['content'],
                                 c.messages_for(data, 'fcl', case)[0]['content'])
            head, tail = c.shared_envelope(data, 'fcl')
            for case, brief in briefs.items():
                self.assertTrue(brief.startswith(head))
                self.assertTrue(brief.endswith(tail))
                self.assertEqual(brief[len(head):len(brief) - len(tail)],
                                 data['arms']['fcl']['cases'][case]['objection_projection'])


# ----------------------------------------------------------------- recoding re-read (2026-09-14)

class RecodingReRead(unittest.TestCase):
    """Pins the findings of the FW5:609 constituent re-read of all 85 units.

    Each assertion below names a unit the adversarial review found altered in a way the
    declared rule set does not license. They are pinned as text, not as a hash, so a
    future edit that reintroduces the fault fails with the unit that caused it.
    """

    @staticmethod
    def _unit(arm, unit_id):
        data = material()
        return next(u for u in data['arms'][arm]['recoding']['units']
                    if u['unit_id'] == unit_id)

    def test_objected_to_items_stay_in_the_objected_to_role(self):
        unit = self._unit('prose', 'B.P5.S2')
        self.assertIn('grounds for objecting to', unit['recoded'])
        self.assertNotIn('My grounds for objecting concern', unit['recoded'])
        for item in ('order of operations', 'diagnostic confidence'):
            self.assertIn(item, unit['original'])
            self.assertIn(item, unit['recoded'])

    def test_the_desert_claim_is_not_flattened_into_a_placement_claim(self):
        for arm, unit_id in (('fcl', 'B.P5.S2'), ('fcl', 'K.c1.text.S1')):
            unit = self._unit(arm, unit_id)
            self.assertIn('deserves to be', unit['original'], unit_id)
            self.assertIn('deserves to be', unit['recoded'], unit_id)

    def test_conditional_form_is_held_constant_in_every_condition_unit(self):
        named = [('fcl', 'K.o1.bearing.S1'), ('fcl', 'K.o4.bearing.S1'), ('fcl', 'K.o4.text.S2'),
                 ('fcl', 'B.P4.S4'), ('fcl', 'B.P6.S4'), ('prose', 'C.P2.S2'),
                 ('prose', 'C.P3.S2'), ('prose', 'B.P4.S2'), ('prose', 'C.P1.S2'),
                 ('prose', 'C.P4.S1'), ('prose', 'C.P6.S1')]
        for arm, unit_id in named:
            unit = self._unit(arm, unit_id)
            self.assertIn('if ', unit['original'].lower(), unit_id)
            self.assertIn('if ', unit['recoded'].lower(), unit_id)
        data = material()
        for arm in ('fcl', 'prose'):
            for unit in data['arms'][arm]['recoding']['units']:
                self.assertEqual(unit['original'].lower().count('if '),
                                 unit['recoded'].lower().count('if '), unit['unit_id'])

    def test_an_open_demonstrative_is_not_resolved_for_the_objection(self):
        unit = self._unit('prose', 'C.P4.S2')
        self.assertTrue(unit['recoded'].startswith('That would be evidence'))
        self.assertNotIn('Such a report', unit['recoded'])

    def test_the_fcl_recoding_introduces_no_typography_the_source_does_not_use(self):
        data = material()
        for arm in ('fcl', 'prose'):
            units = data['arms'][arm]['recoding']['units']
            for char in ('\u2014', '\u2013', '\u2018', '\u2019', '\u201c', '\u201d'):
                self.assertEqual(sum(u['original'].count(char) for u in units),
                                 sum(u['recoded'].count(char) for u in units),
                                 (arm, char))

    def test_r4_is_declared_and_not_exercised_under_its_uniqueness_restriction(self):
        data = material()
        report = c.check_recoding(data)
        for arm in ('fcl', 'prose'):
            rule = data['arms'][arm]['recoding']['rule']
            self.assertIn('unique antecedent inside the same paragraph', rule['R4'])
            self.assertEqual(report[arm]['rule_labels_declared_and_not_used'], ['R4'])
            for unit in data['arms'][arm]['recoding']['units']:
                self.assertNotIn('R4', unit['rules'], unit['unit_id'])

    def test_no_unit_is_the_identity_and_every_label_is_declared(self):
        data = material()
        for arm in ('fcl', 'prose'):
            declared = set(data['arms'][arm]['recoding']['rule'])
            for unit in data['arms'][arm]['recoding']['units']:
                self.assertNotEqual(unit['original'], unit['recoded'], unit['unit_id'])
                self.assertTrue(set(unit['rules']) <= declared, unit['unit_id'])

    def test_hedge_force_is_checked_per_unit_and_a_change_is_refused(self):
        data = material()
        self.assertEqual(c.check_recoding(data)['fcl']['units_hedge_checked'], 50)
        unit = next(u for u in data['arms']['fcl']['recoding']['units']
                    if u['unit_id'] == 'K.o1.bearing.S1')
        unit['recoded'] = unit['recoded'].replace('If the driver is', 'Should the driver be')
        with self.assertRaises(ValueError) as caught:
            c.check_recoding(data)
        self.assertEqual(str(caught.exception), 'RECODING_HEDGE_FORCE_CHANGED')

    def test_a_rewritten_quotation_is_refused(self):
        data = material()
        unit = next(u for u in data['arms']['fcl']['recoding']['units']
                    if u['unit_id'] == 'B.P4.S2')
        unit['recoded'] = unit['recoded'].replace('"thin."', '"sparse."')
        with self.assertRaises(ValueError) as caught:
            c.check_recoding(data)
        self.assertEqual(str(caught.exception), 'RECODING_QUOTATION_CHANGED')

    def test_an_undeclared_rule_label_is_refused(self):
        data = material()
        data['arms']['prose']['recoding']['units'][0]['rules'] = ['R6']
        with self.assertRaises(ValueError) as caught:
            c.check_recoding(data)
        self.assertEqual(str(caught.exception), 'RECODING_UNDECLARED_RULE')

    def test_a_changed_fcl_reference_array_is_refused(self):
        data = material()
        block = data['arms']['fcl']['cases']['recoding']
        doc = json.loads(block['commitments'])
        for record in doc['records']:
            if record.get('target'):
                record['target'] = list(record['target']) + ['account#c3']
                break
        block['commitments'] = json.dumps(doc, ensure_ascii=False, separators=(',', ':'))
        with self.assertRaises(ValueError) as caught:
            c.check_recoding(data)
        self.assertIn(str(caught.exception),
                      {'RECODING_CHANGED_FCL_REFERENCES', 'RECODING_COMMITMENT_NOT_RECONSTRUCTIBLE'})

    def test_a_changed_uptake_list_is_refused(self):
        data = material()
        block = data['arms']['fcl']['cases']['recoding']
        doc = json.loads(block['commitments'])
        doc['uptake'] = list(reversed(doc['uptake']))
        block['commitments'] = json.dumps(doc, ensure_ascii=False, separators=(',', ':'))
        with self.assertRaises(ValueError) as caught:
            c.check_recoding(data)
        self.assertEqual(str(caught.exception), 'RECODING_CHANGED_FCL_UPTAKE')


# ----------------------------------------------------------------- transport pins

class TransportPins(unittest.TestCase):

    def test_the_transport_and_its_registry_are_pinned_and_rehashed(self):
        data = material()
        report = c.check_transport_pins(data)
        self.assertEqual(report['module_sha256'], data['transport_pins']['module_sha256'])
        self.assertEqual(report['registry_sha256'], data['transport_pins']['registry_sha256'])
        self.assertIn('endpoints.json', data['transport_pins']['registry'])
        self.assertIn('provider package', data['transport_pins']['note'])

    def test_a_tampered_transport_pin_stops_the_study(self):
        data = material()
        data['transport_pins']['module_sha256'] = '0' * 64
        with self.assertRaises(ValueError) as caught:
            c.check_transport_pins(data)
        self.assertEqual(str(caught.exception), 'TRANSPORT_PIN_MISMATCH')

    def test_the_pinned_registry_is_the_one_beside_the_resolved_transport(self):
        module = c._provider_module()
        module_path = Path(module.__file__).resolve()
        registry = module_path.parent / 'data' / 'endpoints.json'
        self.assertTrue(registry.exists())
        self.assertEqual(hashlib.sha256(registry.read_bytes()).hexdigest(),
                         material()['transport_pins']['registry_sha256'])
        self.assertEqual(hashlib.sha256(module_path.read_bytes()).hexdigest(),
                         material()['transport_pins']['module_sha256'])
        # the registry, not the repository, is what supplies base_url and chat_path
        for endpoint in material()['endpoints']:
            resolved = module.ENDPOINTS[endpoint['id']]
            self.assertTrue(resolved.base_url)
            self.assertTrue(resolved.chat_path)


# ----------------------------------------------------------------- wave shape

class WaveShape(unittest.TestCase):
    """47 waves, and the one that straddles the credential boundary holds ten.

    The authorisation is five concurrent requests PER CREDENTIAL, not five per wave. The
    coordinate order is endpoint-major, so 46 waves are single-key and hold five, and the
    wave spanning `deepseek-flash`'s last five coordinates and the first Ollama
    endpoint's first five holds ten across two credentials. PLAN section 5 says exactly
    that; an earlier wording claimed every wave was single-key, which was false of this
    one.
    """

    def test_forty_seven_waves_with_one_ten_coordinate_boundary_wave(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
        waves = c.build_waves(plan)
        self.assertEqual(len(waves), 47)
        key_env = {e['slug']: e['key_env'] for e in plan['endpoints']}
        sizes, mixed = [], []
        for wave in waves:
            sizes.append(len(wave['coordinates']))
            keys = {}
            for coord in wave['coordinates']:
                key = key_env[coord['endpoint_slug']]
                keys[key] = keys.get(key, 0) + 1
            self.assertTrue(all(n <= 5 for n in keys.values()), wave['wave_id'])
            if len(keys) > 1:
                mixed.append((wave['wave_id'], dict(sorted(keys.items()))))
        self.assertEqual(sorted(sizes), [5] * 46 + [10])
        self.assertEqual(mixed, [(mixed[0][0], {'DEEPSEEK_API_KEY': 5, 'OLLAMA_API_KEY': 5})])
        self.assertEqual(sum(sizes), 240)

    def test_the_plan_states_the_boundary_wave_rather_than_claiming_single_key(self):
        flat = ' '.join((REGISTER / 'PLAN.md')
                        .read_text(encoding='utf-8').split())
        self.assertNotIn('every wave is single-key, so at most five requests are in flight',
                         flat)
        self.assertIn('46 of the 47 waves are single-key', flat)
        self.assertIn('holds ten', flat)
        self.assertIn('**at most 5 coordinates per credential**', flat)


# ----------------------------------------------------------------- per-endpoint timeout

class PerEndpointTimeout(unittest.TestCase):
    """The wall-clock read timeout is declared per endpoint and applied to the Endpoint.

    F001 occurrences 07 and 08 (REC-20260914-T) took both of their failures on the fixed
    180-second endpoint timeout at the 32768 ceiling -- `TRANSPORT_OR_RESPONSE_ERROR`,
    "The read operation timed out", at 180368 ms (`ollama/glm-5.3`) and 180456 ms
    (`ollama/kimi-k3`). C001 therefore declares the timeout per endpoint, applies it with
    `dataclasses.replace` on the registry `Endpoint` at provider construction, freezes it
    in `plan.json`, records it in every request and receipt, and refuses any disagreement
    with one code, `TIMEOUT_NOT_APPLIED`. `endpoints.json` itself is never written.
    """

    EXPECTED = {'deepseek-flash': 180, 'ollama/gpt-oss-120b': 600,
                'ollama/qwen3.5-397b': 600, 'ollama/glm-5.3': 600,
                'ollama/kimi-k3': 600, 'ollama/gemma4-31b': 600}

    def test_the_declared_table_is_per_endpoint_and_agrees_in_both_published_places(self):
        data = material()
        self.assertEqual(data['ceilings']['timeout_seconds'], self.EXPECTED)
        self.assertEqual(data['ceilings']['timeout_seconds_authorised_maximum'],
                         c.TIMEOUT_SECONDS_AUTHORISED)
        for endpoint in data['endpoints']:
            self.assertEqual(endpoint['timeout_seconds'], self.EXPECTED[endpoint['id']],
                             endpoint['id'])
        policy = data['ceilings']['timeout_seconds_policy']
        for fragment in ('REC-20260914-T', 'occurrence-07', 'occurrence-08', '180368',
                         '180456', 'The read operation timed out', 'dataclasses.replace',
                         'TIMEOUT_NOT_APPLIED', 'NO CELL IS RESCUED'):
            self.assertIn(fragment, policy, fragment)

    def test_600_is_the_transports_own_validation_maximum(self):
        module = c._provider_module()
        base = module.ENDPOINTS['ollama/glm-5.3']
        self.assertEqual(c.TIMEOUT_SECONDS_AUTHORISED, 600)
        raised = dataclasses.replace(base, timeout_seconds=c.TIMEOUT_SECONDS_AUTHORISED)
        self.assertEqual(raised.timeout_seconds, 600)
        with self.assertRaises(ValueError):
            dataclasses.replace(base, timeout_seconds=c.TIMEOUT_SECONDS_AUTHORISED + 1)
        with self.assertRaises(ValueError):
            dataclasses.replace(base, timeout_seconds=0)

    def test_resolve_endpoint_applies_it_and_changes_nothing_else(self):
        module = c._provider_module()
        for endpoint in material()['endpoints']:
            registry = module.ENDPOINTS[endpoint['id']]
            applied = c.resolve_endpoint(endpoint)
            self.assertEqual(applied.timeout_seconds, self.EXPECTED[endpoint['id']])
            self.assertEqual(
                dataclasses.replace(applied, timeout_seconds=registry.timeout_seconds),
                registry, endpoint['id'])

    def test_the_published_registry_file_is_not_edited(self):
        """The raise reaches the wire without touching a file other plans pin."""
        module = c._provider_module()
        registry = Path(module.__file__).resolve().parent / 'data' / 'endpoints.json'
        raw = json.loads(registry.read_text(encoding='utf-8'))
        declared = {row['name']: row.get('timeout_seconds', 180) for row in raw['endpoints']}
        for name in self.EXPECTED:
            self.assertEqual(declared[name], 180, name)
        pins = material()['transport_pins']
        self.assertEqual(hashlib.sha256(registry.read_bytes()).hexdigest(),
                         pins['registry_sha256'])

    def test_a_declared_timeout_outside_the_transport_range_is_refused(self):
        data = json.loads(MATERIAL.read_bytes())
        data['endpoints'][1]['timeout_seconds'] = 601
        data['ceilings']['timeout_seconds'][data['endpoints'][1]['id']] = 601
        with self.assertRaises(ValueError) as caught:
            c.validate_material(data)
        self.assertEqual(str(caught.exception), 'MATERIAL_ENDPOINT_TIMEOUT_SECONDS')

    def test_a_material_whose_timeout_tables_disagree_is_refused(self):
        data = json.loads(MATERIAL.read_bytes())
        data['endpoints'][1]['timeout_seconds'] = 180
        with self.assertRaises(ValueError) as caught:
            c.validate_material(data)
        self.assertEqual(str(caught.exception), 'MATERIAL_ENDPOINT_TIMEOUT_SECONDS')

    def test_an_endpoint_carrying_no_declared_timeout_is_refused(self):
        endpoint = dict(next(e for e in material()['endpoints'] if e['id'] == 'ollama/kimi-k3'))
        endpoint.pop('timeout_seconds')
        with self.assertRaises(ValueError) as caught:
            c.resolve_endpoint(endpoint)
        self.assertEqual(str(caught.exception), 'TIMEOUT_NOT_APPLIED')

    def test_the_plan_freezes_the_timeout_per_endpoint(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
        self.assertEqual({e['id']: e['timeout_seconds'] for e in plan['endpoints']},
                         self.EXPECTED)
        self.assertEqual(plan['ceilings']['timeout_seconds'], self.EXPECTED)

    def test_a_transport_reporting_another_timeout_is_refused(self):
        """The preflight reads the timeout off the provider it built, not off the material."""
        import tempfile
        data = material()
        plan = c.plan_body(data, MATERIAL.read_bytes(), b'helper')
        plan['plan_id'] = c.digest(plan)
        original = c._offline_provider

        def stale(endpoint, root):
            provider, source = original(endpoint, root)
            object.__setattr__(
                provider, 'endpoint',
                dataclasses.replace(provider.endpoint, timeout_seconds=180))
            return provider, source

        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError) as caught:
                c._offline_preflight(data, plan, stale, Path(tmp))
        self.assertEqual(str(caught.exception), 'TIMEOUT_NOT_APPLIED')

    def test_the_timeout_is_not_a_payload_field(self):
        """A socket setting, not a wire parameter: the request bytes are unchanged by it."""
        data = material()
        endpoint = next(e for e in data['endpoints'] if e['id'] == 'ollama/glm-5.3')
        coord = c.coordinate(endpoint['slug'], 'fcl', 'original', 1)
        messages = c.messages_for(data, 'fcl', 'original')
        at_600 = c.payload_for(messages, c.spec_for(endpoint, coord))
        at_180 = c.payload_for(messages, c.spec_for({**endpoint, 'timeout_seconds': 180}, coord))
        self.assertEqual(c.digest(at_600), c.digest(at_180))
        self.assertNotIn('timeout', json.dumps(at_600))

    def test_every_request_and_receipt_records_the_applied_timeout(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset(replies=Comparison._replies())
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['arm'] == 'fcl' and coord['case'] == 'original'
                  and coord['replicate'] == 1)
            plan = json.loads((out / 'plan.json').read_bytes())
            seen = 0
            for endpoint in plan['endpoints']:
                coord = c.coordinate(endpoint['slug'], 'fcl', 'original', 1)
                request = json.loads(c.at(out, 'requests', coord).read_bytes())
                receipt = json.loads(c.at(out, 'responses', coord).read_bytes())
                self.assertEqual(request['timeout_seconds'], self.EXPECTED[endpoint['id']])
                self.assertEqual(request['spec']['timeout_seconds'],
                                 self.EXPECTED[endpoint['id']])
                self.assertEqual(receipt['timeout_seconds'], self.EXPECTED[endpoint['id']])
                seen += 1
            self.assertEqual(seen, 6)
            report = c.audit(out, REPO)
            self.assertEqual(report['timeout_seconds_by_endpoint'], self.EXPECTED)

    def test_a_record_claiming_another_timeout_fails_the_audit(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset(replies=Comparison._replies())
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['endpoint_slug'] == 'ollama-glm-5.3'
                  and coord['arm'] == 'fcl' and coord['case'] == 'original'
                  and coord['replicate'] == 1)
            coord = c.coordinate('ollama-glm-5.3', 'fcl', 'original', 1)

            def rewrite(path, mutate):
                data = json.loads(path.read_bytes())
                mutate(data)
                path.write_bytes(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                            indent=2).encode() + b'\n')
                return data

            request_path = c.at(out, 'requests', coord)
            self.assertEqual(json.loads(request_path.read_bytes())['timeout_seconds'], 600)

            def downgrade(request):
                request['timeout_seconds'] = 180
                request['spec']['timeout_seconds'] = 180

            # The tamperer also refreshes every internal cross-reference, so the record
            # set stays perfectly self-consistent about a configuration the plan froze
            # otherwise. Only the tie back to the plan catches it.
            request = rewrite(request_path, downgrade)
            rewrite(c.at(out, 'attempts', coord),
                    lambda a: a.update({'request_sha256': c.digest(request)}))
            rewrite(c.at(out, 'responses', coord),
                    lambda r: r.update({'request_sha256': c.digest(request),
                                        'timeout_seconds': 180}))
            with self.assertRaises(ValueError) as caught:
                c.audit(out, REPO)
            self.assertEqual(str(caught.exception), 'TIMEOUT_NOT_APPLIED')


# ----------------------------------------------------------------- pre-declared reading rule

class ReadingRule(unittest.TestCase):

    def test_the_reading_rule_is_inside_the_frozen_identity(self):
        import tempfile
        data = material()
        rule = data['reading_rule']
        self.assertEqual([r['id'] for r in rule['registers']], ['T', 'E', 'D', 'G'])
        self.assertEqual(rule['marks'], ['differs', 'same', 'unresolved'])
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            plan = json.loads((out / 'plan.json').read_bytes())
            self.assertEqual(plan['reading_rule'], rule)

    def test_a_missing_reading_rule_is_refused(self):
        data = material()
        data.pop('reading_rule')
        with self.assertRaises(ValueError) as caught:
            c.validate_material(data)
        self.assertEqual(str(caught.exception), 'MATERIAL_READING_RULE')

    def test_the_rendered_comparison_carries_the_registers_and_empty_marks(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = Comparison()._run_and_table(Path(tmp))
            rendered = (out / 'COMPARISON.md').read_text(encoding='utf-8')
            self.assertIn('What "differs" means, pre-declared', rendered)
            for name in ('T target named', 'E objection record engaged',
                         'D proposed action', 'G grounds cited'):
                self.assertIn(name, rendered)
            self.assertIn('ORIGINAL vs CONTROL |  |  |  |  |', rendered)
            data = json.loads((out / 'comparison.json').read_bytes())
            for entry in data['tables']:
                for row in entry['root_register_marks'].values():
                    self.assertEqual(set(row), {'T', 'E', 'D', 'G'})
                    self.assertTrue(all(v == '' for v in row.values()))


# ----------------------------------------------------------------- reference disambiguation

class ReferenceDisambiguation(unittest.TestCase):

    @staticmethod
    def _addresses(arm='fcl'):
        return material()['arms'][arm]['artifact_addresses']

    def _doc(self, refs):
        return json.dumps({'language': 'FCL-1', 'records': [
            {'id': 'k1', 'type': 'use', 'text': 't', 'target': list(refs)}], 'uptake': ['k1']})

    def test_the_artifact_addresses_are_declared_and_distinct(self):
        for arm in ('fcl', 'prose'):
            addresses = self._addresses(arm)
            self.assertEqual(len({addresses[n] for n in ('objection', 'account', 'rival')}), 3)
            self.assertEqual(addresses['truncation_chars'], 16)

    def test_an_account_prefixed_ref_is_not_counted_as_an_objection_ref(self):
        addresses = self._addresses()
        ids = material()['arms']['fcl']['objection_source']['record_ids']
        surface = c.fcl_surface(self._doc([addresses['account'] + '#c1',
                                           addresses['objection'] + '#o2']), ids, addresses)
        self.assertEqual(surface['objection_record_ids_in_refs'], ['o2'])
        self.assertEqual(surface['account_prefixed_refs'], ['c1'])
        self.assertEqual(surface['rival_prefixed_refs'], [])

    def test_the_sixteen_hex_truncation_the_h005_node_emitted_resolves(self):
        addresses = self._addresses()
        ids = material()['arms']['fcl']['objection_source']['record_ids']
        surface = c.fcl_surface(self._doc([addresses['objection'][:16] + '#c2',
                                           addresses['account'][:16] + '#c1',
                                           addresses['rival'][:16] + '#r1']), ids, addresses)
        self.assertEqual(surface['objection_record_ids_in_refs'], ['c2'])
        self.assertEqual(surface['account_prefixed_refs'], ['c1'])
        self.assertEqual(surface['rival_prefixed_refs'], ['r1'])
        self.assertEqual(surface['ref_prefix_forms'], {'TRUNCATED_ADDRESS': 3})

    def test_an_unrecognised_prefix_is_reported_and_not_attributed(self):
        addresses = self._addresses()
        ids = material()['arms']['fcl']['objection_source']['record_ids']
        surface = c.fcl_surface(self._doc(['deadbeefdeadbeef#o1']), ids, addresses)
        self.assertEqual(surface['objection_record_ids_in_refs'], [])
        self.assertEqual(surface['unresolved_prefix_refs'], ['deadbeefdeadbeef#o1'])

    def test_a_bare_ref_stays_in_the_unresolved_channel(self):
        addresses = self._addresses()
        ids = material()['arms']['fcl']['objection_source']['record_ids']
        surface = c.fcl_surface(self._doc(['o1']), ids, addresses)
        self.assertEqual(surface['objection_record_ids_in_refs'], [])
        self.assertEqual(surface['bare_refs_unresolved'], ['o1'])

    def test_the_bare_token_channel_does_not_double_count_a_structured_ref(self):
        addresses = self._addresses()
        text = addresses['objection'][:16] + '#o1 and a bare o1 and record.o1 and o1'
        self.assertEqual(c.token_occurrences(text, ['o1']), {'o1': 2})
        self.assertEqual(c.token_occurrences('o1#x', ['o1']), {'o1': 1})
        self.assertEqual(c.token_occurrences('deadbeef#o1', ['o1']), {})

    def test_notes_no_longer_call_a_bare_structured_ref_unambiguous(self):
        notes = (REGISTER / 'NOTES.md').read_text(
            encoding='utf-8')
        self.assertIn('only when its prefix is retained', notes)


# ----------------------------------------------------------------- audit re-ties to the plan

class AuditTiesToThePlan(unittest.TestCase):

    def _occurrence(self, tmp: Path):
        out, result = prepared(tmp)
        ScriptedProvider.reset(replies=Comparison._replies())
        c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
              notify=lambda _: None,
              only=lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
              and coord['arm'] == 'fcl')
        return out

    @staticmethod
    def _rewrite(path: Path, mutate):
        data = json.loads(path.read_bytes())
        mutate(data)
        path.write_bytes(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                    indent=2).encode() + b'\n')
        return data

    def test_a_request_carrying_another_cases_brief_is_refused(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = self._occurrence(Path(tmp))
            data = material()
            coord = c.coordinate('deepseek-flash', 'fcl', 'control', 1)
            request_path = c.at(out, 'requests', coord)

            def swap(request):
                messages = c.messages_for(data, 'fcl', 'original')
                request['messages'] = messages
                request['messages_sha256'] = c.digest(messages)
                request['provider_payload'] = c.payload_for(messages, request['spec'])
                request['provider_payload_sha256'] = c.digest(request['provider_payload'])

            request = self._rewrite(request_path, swap)
            # the tamperer also refreshes every internal cross-reference, which is all
            # the old audit ever checked.
            self._rewrite(c.at(out, 'attempts', coord),
                          lambda a: a.update({'request_sha256': c.digest(request)}))
            self._rewrite(c.at(out, 'responses', coord),
                          lambda r: r.update({'request_sha256': c.digest(request)}))
            with self.assertRaises(ValueError) as caught:
                c.audit(out, REPO)
            self.assertEqual(str(caught.exception), 'REQUEST_NOT_FROM_PLAN')

    def test_a_foreign_plan_id_on_a_request_is_refused(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = self._occurrence(Path(tmp))
            coord = c.coordinate('deepseek-flash', 'fcl', 'original', 1)
            request = self._rewrite(c.at(out, 'requests', coord),
                                    lambda r: r.update({'plan_id': '0' * 64}))
            self._rewrite(c.at(out, 'attempts', coord),
                          lambda a: a.update({'request_sha256': c.digest(request)}))
            self._rewrite(c.at(out, 'responses', coord),
                          lambda r: r.update({'request_sha256': c.digest(request)}))
            with self.assertRaises(ValueError) as caught:
                c.audit(out, REPO)
            self.assertEqual(str(caught.exception), 'REQUEST_NOT_FROM_PLAN')

    def test_an_artifact_body_that_was_never_delivered_is_refused(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = self._occurrence(Path(tmp))
            coord = c.coordinate('deepseek-flash', 'fcl', 'recoding', 1)
            path = c.at(out, 'artifacts', coord)
            self._rewrite(path, lambda a: a.update({'body': 'TAMPERED TEXT NEVER DELIVERED'}))
            self._rewrite(c.at(out, 'responses', coord),
                          lambda r: r.update({'artifact_sha256': c.sha(path.read_bytes())}))
            with self.assertRaises(ValueError) as caught:
                c.audit(out, REPO)
            self.assertEqual(str(caught.exception), 'ARTIFACT_NOT_DERIVED_FROM_DELIVERY')

    def test_a_clean_occurrence_still_audits(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = self._occurrence(Path(tmp))
            report = c.audit(out, REPO)
            self.assertEqual(report['counts']['COMPLETE'], 19)
            self.assertEqual(report['counts']['PARTIAL'], 1)
            self.assertEqual(report['failure_codes'], {})


# ----------------------------------------------------------------- failure codes and refusals

class FailureRecording(unittest.TestCase):

    def test_a_declared_refusal_code_reaches_the_receipt_and_the_audit(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            replies = dict(Comparison._replies())
            replies['deepseek-flash/fcl/original/rep3'] = {
                'content': 'THE MODEL SAID SOMETHING ROOT SHOULD READ',
                'status': 'EMPTY_GENERATION', 'finish_reason': 'stop'}
            ScriptedProvider.reset(replies=replies)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                  and coord['arm'] == 'fcl')
            coord = c.coordinate('deepseek-flash', 'fcl', 'original', 3)
            receipt = json.loads(c.at(out, 'responses', coord).read_bytes())
            self.assertEqual(receipt['status'], 'FAILED')
            self.assertEqual(receipt['validation_failure_type'], 'PROVIDER_NOT_USABLE')
            self.assertEqual(receipt['validation_failure_class'], 'ValueError')
            report = c.audit(out, REPO)
            self.assertEqual(report['failure_codes'], {'PROVIDER_NOT_USABLE': 1})

    def test_a_refused_delivery_still_shows_root_the_delivered_bytes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            replies = dict(Comparison._replies())
            replies['deepseek-flash/fcl/original/rep3'] = {
                'content': 'THE MODEL SAID SOMETHING ROOT SHOULD READ',
                'status': 'EMPTY_GENERATION', 'finish_reason': 'stop'}
            ScriptedProvider.reset(replies=replies)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['endpoint_slug'] == 'deepseek-flash')
            c.table(out, REPO, force=True)
            rendered = (out / 'juxtaposition/deepseek-flash__fcl.md').read_text(encoding='utf-8')
            self.assertIn('ROOT SHOULD READ', rendered)
            self.assertIn('Delivery was NOT accepted: `PROVIDER_NOT_USABLE`', rendered)
            data = json.loads((out / 'comparison.json').read_bytes())
            fcl = next(t for t in data['tables'] if t['arm'] == 'fcl')
            row = next(r for r in fcl['cases']['original'] if r['replicate'] == 3)
            self.assertEqual(row['state'], 'FAILED')
            self.assertTrue(row['path'].endswith('rep3.txt'))
            self.assertIn('original/rep3', fcl['unresolved_cells'])

    def test_no_delivered_text_says_so_rather_than_pretending(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = Comparison()._run_and_table(Path(tmp))
            rendered = (out / 'juxtaposition/deepseek-flash__prose.md').read_text(encoding='utf-8')
            self.assertNotIn('(no delivered text reached disk)', rendered)

    def test_failure_code_prefers_the_declared_code_over_the_class(self):
        module = c._provider_module()
        self.assertEqual(c.failure_code(module.ProviderFailure('HTTP_429', 'slow down')), 'HTTP_429')
        self.assertEqual(c.failure_code(ValueError('PROVIDER_NOT_USABLE')), 'PROVIDER_NOT_USABLE')
        self.assertEqual(c.failure_code(ValueError('not a code')), 'ValueError')


# ----------------------------------------------------------------- resume

class Resume(unittest.TestCase):

    def test_resume_completes_an_interrupted_case_without_replaying_it(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset()
            first = (lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                     and coord['arm'] == 'fcl' and coord['case'] == 'original'
                     and coord['replicate'] <= 2)
            whole = (lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                     and coord['arm'] == 'fcl' and coord['case'] == 'original')
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None, only=first)
            with self.assertRaises(FileExistsError):
                c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                      notify=lambda _: None, only=whole)
            report = c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                           notify=lambda _: None, only=whole, resume=True)
            self.assertTrue(report['resumed'])
            self.assertEqual(report['skipped_already_terminal'], 2)
            self.assertEqual(report['dispatched'], 3)
            for replicate in range(1, 6):
                coord = c.coordinate('deepseek-flash', 'fcl', 'original', replicate)
                self.assertTrue(c.at(out, 'responses', coord).exists())
            c.audit(out, REPO)

    def test_resume_still_refuses_a_request_without_a_receipt(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset()
            only = (lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                    and coord['arm'] == 'fcl' and coord['case'] == 'original'
                    and coord['replicate'] == 1)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None, only=only)
            coord = c.coordinate('deepseek-flash', 'fcl', 'original', 1)
            c.at(out, 'responses', coord).unlink()
            with self.assertRaises(FileExistsError) as caught:
                c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                      notify=lambda _: None, only=only, resume=True)
            self.assertEqual(str(caught.exception), 'NO_REPLAY')

    def test_the_wave_record_is_idempotent_across_a_resume(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            ScriptedProvider.reset()
            only = (lambda coord: coord['endpoint_slug'] == 'deepseek-flash'
                    and coord['arm'] == 'fcl' and coord['case'] == 'original')
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: only(coord) and coord['replicate'] == 1)
            before = sorted(p.name for p in (out / 'waves').iterdir())
            waves = {p.name: p.read_bytes() for p in (out / 'waves').iterdir()}
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: only(coord) and coord['replicate'] == 1, resume=True)
            self.assertEqual(sorted(p.name for p in (out / 'waves').iterdir()), before)
            self.assertEqual({p.name: p.read_bytes() for p in (out / 'waves').iterdir()}, waves)


# ----------------------------------------------------------------- guards with teeth

class GuardsWithTeeth(unittest.TestCase):

    def test_a_scoring_key_anywhere_is_refused(self):
        for value in ({'score': 1},
                      {'tables': [{'root_reading': {'rank': ''}}]},
                      {'a': {'b': [{'c': {'verdict': 'x'}}]}},
                      [[{'weight': 0.5}]]):
            with self.assertRaises(ValueError) as caught:
                c.assert_no_scoring_keys(value)
            self.assertEqual(str(caught.exception), 'SCORING_KEY_FORBIDDEN')

    def test_a_scoring_key_is_recognised_whatever_its_case(self):
        with self.assertRaises(ValueError):
            c.assert_no_scoring_keys({'QUALITY': 'high'})

    def test_an_innocent_dict_passes(self):
        c.assert_no_scoring_keys({'record_ids': ['o1'], 'counts': {'COMPLETE': 3}})

    def test_the_preflight_call_count_assertion_can_actually_fail(self):
        import tempfile

        class Calling:
            """An OfflineProvider stand-in that moves the counter the preflight reads."""

            calls = 0

            def __init__(self, endpoint, records):
                self.endpoint = endpoint

            def _validate_call_args(self, **kwargs):
                pass

            def _check_json_mode_prompt(self, *args):
                pass

            def _settings_view(self, **call):
                return {'timeout_seconds': self.endpoint['timeout_seconds'],
                        'max_concurrency': 1, **call}

            def _build_payload(self, messages, *, response_format, max_tokens, temperature,
                               seed, thinking, reasoning_effort, extra):
                type(self).calls += 1
                payload = {'model': self.endpoint['model'],
                           'messages': [dict(m) for m in messages], 'stream': False,
                           'max_tokens': max_tokens, 'response_format': dict(response_format)}
                if seed is not None:
                    payload['seed'] = seed
                return payload

        Calling.calls = 0
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError) as caught:
                c.prepare(MATERIAL, Path(tmp) / 'occ', REPO,
                          offline_provider_factory=lambda endpoint, root: (
                              Calling(endpoint, root), 'test.Calling'))
            self.assertEqual(str(caught.exception), 'OFFLINE_PREFLIGHT_MADE_A_PROVIDER_CALL')
        self.assertGreater(Calling.calls, 0)

    def test_the_preflight_builds_every_payload_through_the_transport(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            preflight = json.loads((out / 'preflight.json').read_bytes())
            self.assertEqual(preflight['payloads_built_by_the_transport'], 240)
            self.assertEqual(preflight['provider_calls'], 0)
            self.assertIn('transport_pins_verified', preflight)

    def test_the_preflight_leaves_no_temporary_directories_behind(self):
        import glob
        import tempfile
        before = set(glob.glob('/tmp/c001-preflight-*'))
        with tempfile.TemporaryDirectory() as tmp:
            prepared(Path(tmp))
        self.assertEqual(set(glob.glob('/tmp/c001-preflight-*')) - before, set())

    def test_the_suite_hardcodes_no_session_staging_path(self):
        # assembled from parts so this assertion is not itself the thing it forbids
        marker = '/' + 'tmp/' + 'claude-'
        source = Path(__file__).read_text(encoding='utf-8')
        self.assertNotIn(marker, source)
        self.assertNotIn('environ.' + 'setdefault', source)
        for driver_source in (V1_SOURCE, V2_SOURCE):
            self.assertNotIn(marker, driver_source.read_text(encoding='utf-8'))
        notes = (REGISTER / 'NOTES.md').read_text(
            encoding='utf-8')
        self.assertIn('BEFORE publication only', notes)

    def test_the_scanned_credential_names_are_derived_from_the_material(self):
        c.register_credential_envs(material())
        names = c.scanned_credential_envs()
        for endpoint in material()['endpoints']:
            self.assertIn(endpoint['key_env'], names)
        self.assertIn('DEEPSEEK_API_KEY', names)
        self.assertIn('OLLAMA_API_KEY', names)

    def test_markdown_cells_escape_pipes_and_newlines_everywhere(self):
        self.assertEqual(c._md('a|b'), 'a\\|b')
        self.assertEqual(c._md(['a|b', 'c\nd']), 'a\\|b, c d')
        self.assertEqual(c._md({'x|y': 'p\nq'}), 'x\\|y=p q')

    def test_a_model_emitted_pipe_cannot_break_the_rendered_table(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = prepared(Path(tmp))
            hostile = json.dumps({'body': 'b', 'commitments': json.dumps({
                'language': 'FCL-1',
                'records': [{'id': 'k|1', 'type': 'use', 'text': 't',
                             'target': ['objection#o1\nsecond line']}],
                'uptake': ['k|1']})})
            replies = {f'deepseek-flash/fcl/{case}/rep{rep}': {'content': hostile}
                       for case in c.CASES for rep in range(1, 6)}
            replies.update({f'deepseek-flash/prose/{case}/rep{rep}':
                            {'content': json.dumps({'body': 'b', 'commitments': 'k'})}
                            for case in c.CASES for rep in range(1, 6)})
            ScriptedProvider.reset(replies=replies)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda _: None,
                  only=lambda coord: coord['endpoint_slug'] == 'deepseek-flash')
            c.table(out, REPO, force=True)
            rendered = (out / 'COMPARISON.md').read_text(encoding='utf-8')
            cells = re.compile(r'(?<!\\)\|')
            head = next(line for line in rendered.splitlines()
                        if line.startswith('| case | rep | delivery | envelope | repairs | '
                                           'strict parse | comparable | fcl parse'))
            width = len(cells.split(head))
            self.assertEqual(width, len(c.FCL_HEAD) + 2)
            checked = 0
            for line in rendered.splitlines():
                if line.startswith('| original | 1 |') or line.startswith('| carrier | 1 |'):
                    if 'fcl parse' in head and 'OK' in line:
                        self.assertEqual(len(cells.split(line)), width, line)
                        checked += 1
            self.assertGreaterEqual(checked, 2)
            self.assertIn('k\\|1', rendered)


# ----------------------------------------------------------------- seed reporting

class SeedReporting(unittest.TestCase):

    def test_seed_echo_is_unknown_rather_than_denied(self):
        record, payload = Decoding()._record(json.dumps({'body': 'b', 'commitments': 'k'}))
        out = c.decode_contribution(record, payload, Decoding()._spec())
        self.assertIsNone(out['seed_echoed_in_response'])
        self.assertFalse(out['seed_echo_reported'])
        self.assertIsNone(out['system_fingerprint'])

    def test_a_returned_seed_and_fingerprint_are_recorded_as_returned(self):
        record, payload = Decoding()._record(json.dumps({'body': 'b', 'commitments': 'k'}),
                                             seed=7, system_fingerprint='fp_abc')
        out = c.decode_contribution(record, payload, Decoding()._spec())
        self.assertEqual(out['seed_echoed_in_response'], 7)
        self.assertTrue(out['seed_echo_reported'])
        self.assertEqual(out['system_fingerprint'], 'fp_abc')

    def test_seed_by_endpoint_aggregates_over_replicates(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = Comparison()._run_and_table(Path(tmp))
            report = c.audit(out, REPO)
            entry = report['seed_by_endpoint']['deepseek-flash']
            self.assertEqual(entry['seeds_sent'], [1, 2, 3, 4, 5])
            self.assertEqual(entry['coordinates'], 40)
            self.assertTrue(entry['honors_seed_constant'])


# ----------------------------------------------------------------- the pre-registration text

class PreRegistrationDocument(unittest.TestCase):
    """PLAN.md is the published pre-registration, so its load-bearing sentences are pinned.

    These are text assertions on purpose: each one names a claim the adversarial review
    found missing, overreaching or wrong, and a later edit that removes it should fail
    here rather than be noticed by the next reviewer.
    """

    @staticmethod
    def _plan():
        return (REGISTER / 'PLAN.md').read_text(
            encoding='utf-8')

    @staticmethod
    def _flat():
        """The plan with line wrapping collapsed, so an assertion pins the sentence and
        not the column at which it happens to wrap."""
        return ' '.join((REGISTER / 'PLAN.md')
                        .read_text(encoding='utf-8').split())

    def test_the_plan_states_the_current_material_and_plan_id(self):
        # V2: PLAN.md's "plan identity" row names OCCURRENCE-01's identity, which is the
        # v1 driver's. Recomputing it here with v2 would assert that the register names an
        # identity it was published before -- so the id is minted with the PUBLISHED v1
        # driver, exactly as occurrence-01 minted it, and the assertion keeps its teeth:
        # an edit to the material or to v1 still fails here. v2's own identity is pinned
        # separately, in DispatchScope.test_the_occurrence_02_plan_id_is_stable.
        import tempfile
        plan = self._plan()
        digest = hashlib.sha256(MATERIAL.read_bytes()).hexdigest()
        self.assertIn(digest, plan)
        raw = MATERIAL.read_bytes()
        body = v1.plan_body(v1.validate_material(json.loads(raw)), raw,
                            V1_SOURCE.read_bytes())
        self.assertIn(v1.digest(body), plan)
        with tempfile.TemporaryDirectory() as tmp:
            _, result = prepared(Path(tmp))
        self.assertNotIn(result['plan_id'], plan)
        self.assertNotEqual(result['plan_id'], v1.digest(body))

    def test_section_8a_is_present_and_mirrored_into_the_material(self):
        plan = self._plan()
        self.assertIn('## 8a. What "differs" means, pre-declared', plan)
        for fragment in ('T \u2014 target named', 'E \u2014 objection record engaged, prefix-resolved',
                         'D \u2014 proposed action (disposition)', 'G \u2014 grounds cited',
                         'The replicate baseline, as a rule', 'Order of reading',
                         'Register-to-falsifier mapping', 'Two readers'):
            self.assertIn(fragment, plan)
        rule = material()['reading_rule']
        self.assertIn(rule['registers'][1]['name'], plan)

    def test_the_claim_ceiling_no_longer_claims_to_exclude_the_rivals(self):
        plan = self._plan()
        flat = self._flat()
        self.assertNotIn('inconsistent with the two rival explanations this design can exclude',
                         flat)
        self.assertIn('do not exhibit the differences a coding-tracking or a '
                      'carrier-tracking explanation predicts', flat)
        self.assertIn('A null on the recoding and carrier legs does not exclude those '
                      'explanations; at N = 5 it leaves them unrefuted and unsupported at '
                      'this node', flat)
        self.assertIn('An unresolved cell stays unresolved', plan)

    def test_the_new_limitations_are_recorded(self):
        plan = self._plan()
        self.assertIn('**L8 \u2014 redundancy can conceal use in endpoint invariance.**', plan)
        self.assertIn('**L9 \u2014 the carrier leg is not comparable across arms.**', plan)
        self.assertIn('Original body SHA256', plan)

    def test_the_block_level_length_basis_is_reported(self):
        plan = self._plan()
        self.assertIn('Block level', plan)
        self.assertIn('+7.3 %', plan)
        self.assertIn('indent=2', plan)

    def test_the_interpretation_registry_names_component_edit_semantics(self):
        plan = self._plan()
        self.assertIn('| component edit semantics |', plan)
        for kind in ('RECODING', 'CARRIER', 'CONTROL'):
            self.assertIn('**%s** edit' % kind, plan)

    def test_no_information_structure_or_determiner_rule_is_declared(self):
        data = material()
        for arm in ('fcl', 'prose'):
            self.assertEqual(sorted(data['arms'][arm]['recoding']['rule']),
                             ['R1', 'R2', 'R3', 'R4', 'R5'])
        flat = self._flat()
        self.assertIn('There is **no** rule for information structure', flat)
        self.assertIn('**no** rule for determiner or definiteness change', flat)
        self.assertIn('reverted to the simplest declared operation', flat)

    def test_section_5_and_6_state_the_raised_ollama_ceiling_and_its_evidence(self):
        flat = self._flat()
        data = material()
        self.assertIn('**declared per endpoint**', flat)
        self.assertIn('REC-20260914-S', flat)
        self.assertIn('experiments/diagnostics/F001-fork5-multifamily', flat)
        self.assertIn('occurrence-04', flat)
        self.assertIn('occurrence-05', flat)
        self.assertIn('INCOMPLETE_GENERATION', flat)
        self.assertIn('Raising the ceiling **does not manipulate reasoning.**', flat)
        self.assertIn('not a native-reasoning comparison', flat)
        self.assertIn('A cell that hits even the raised ceiling is still unresolved', flat)
        self.assertIn('**The raised ceiling rescues no cell**', flat)
        for endpoint in data['endpoints']:
            self.assertIn('`%s` |' % endpoint['id'], flat, endpoint['id'])
            self.assertIn(str(endpoint['max_tokens']), flat, endpoint['id'])
        self.assertIn(str(data['ceilings']['max_tokens_authorised_maximum']), flat)
        self.assertGreaterEqual(flat.count('**32768**'), 5)  # one row per Ollama endpoint

    def test_section_5_and_6_state_the_per_endpoint_timeout_and_cite_07_08(self):
        flat = self._flat()
        data = material()
        self.assertIn('The per-endpoint wall-clock timeout', flat)
        self.assertIn('REC-20260914-T', flat)
        # the two records the raise rests on, named so a reader can open them
        for fragment in (
                'occurrence-07/responses/daily/mini_fcl/cycle01/objection.json',
                'occurrence-08/responses/daily/mini_fcl/cycle01/carry.json',
                'occurrence-07/provider/daily/mini_fcl/cycle01/objection/'
                'call-0001.response.json',
                'occurrence-08/provider/daily/mini_fcl/cycle01/carry/call-0001.response.json',
                '180368', '180456', 'The read operation timed out',
                'TRANSPORT_OR_RESPONSE_ERROR', '`ollama/glm-5.3`', '`ollama/kimi-k3`'):
            self.assertIn(fragment, flat, fragment)
        # the mechanism, the bound and the refusal code
        self.assertIn('dataclasses.replace', flat)
        self.assertIn('TIMEOUT_NOT_APPLIED', flat)
        self.assertIn("**transport's own validation maximum**", flat)
        self.assertIn('`src/minireason/data/endpoints.json` is not edited', flat)
        self.assertIn('**no cell is rescued by it.**', flat)
        self.assertIn('The wall-clock timeout is per endpoint, where F001', flat)
        # every declared value appears in the plan's own endpoint table
        for endpoint in data['endpoints']:
            self.assertIn('%d s' % endpoint['timeout_seconds'], flat, endpoint['id'])
        self.assertGreaterEqual(flat.count('**600 s**'), 5)
        self.assertIn(str(data['ceilings']['timeout_seconds_authorised_maximum']), flat)

    def test_the_transport_pins_are_published_and_section_13_names_them(self):
        plan = self._plan()
        pins = material()['transport_pins']
        self.assertIn(pins['module_sha256'], plan)
        self.assertIn(pins['registry_sha256'], plan)
        flat = self._flat()
        self.assertIn("or the transport module's or endpoint registry's bytes", flat)
        # Corrected before dispatch: both pinned files are published repository files
        # now, and the plan may not say otherwise while pinning their bytes.
        self.assertNotIn('the endpoint registry is supplied by the staged `minireason` provider '
                         'package, not by the repository', flat)
        self.assertIn('the endpoint registry and the transport module are the **published '
                      'repository files**', flat)
        self.assertIn('TRANSPORT_PIN_MISMATCH', plan)
        for name in ('src/minireason/provider_openai_compat.py',
                     'src/minireason/data/endpoints.json'):
            self.assertIn(name, plan)

    def test_the_lengths_reported_are_the_lengths_measured(self):
        data = material()
        plan = self._plan()
        for arm in ('fcl', 'prose'):
            head, tail = c.shared_envelope(data, arm)
            self.assertIn(str(len(head)), plan)
            self.assertIn(str(len(tail)), plan)
            for case in c.CASES:
                self.assertIn(str(len(c.brief_for(data, arm, case))), plan)
                self.assertIn(str(len(data['arms'][arm]['cases'][case]['objection_projection'])),
                              plan)


# ----------------------------------------------------------------- premature render

class PrematureRender(unittest.TestCase):

    def test_table_refuses_an_incomplete_occurrence_unless_forced(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, _ = prepared(Path(tmp))
            with self.assertRaises(ValueError) as caught:
                c.table(out, REPO)
            self.assertEqual(str(caught.exception), 'OCCURRENCE_INCOMPLETE')
            self.assertFalse((out / 'comparison.json').exists())
            self.assertFalse((out / 'COMPARISON.md').exists())
            self.assertFalse((out / 'juxtaposition').exists())
            forced = c.table(out, REPO, force=True)
            self.assertEqual(forced['tables'], 12)


# ----------------------------------------------------------------- V2: the fork itself

def _normalised(source: Path) -> list[str]:
    """A driver's source with its module docstring removed, as a list of lines.

    The two files' docstrings differ by construction -- v2's names the bytes it copied
    and lists its own differences -- so comparing them would drown the real diff. Every
    other line is compared exactly.
    """
    import ast
    text = source.read_text(encoding='utf-8')
    tree = ast.parse(text)
    doc = tree.body[0]
    lines = text.splitlines()
    if not (isinstance(doc, ast.Expr) and isinstance(doc.value, ast.Constant)
            and isinstance(doc.value.value, str)):
        raise AssertionError('MODULE_DOCSTRING_EXPECTED')
    del lines[doc.lineno - 1:doc.end_lineno]
    return lines


def _definitions(source: Path) -> dict[str, str]:
    """Top-level def/class names mapped to their exact source segment."""
    import ast
    text = source.read_text(encoding='utf-8')
    tree = ast.parse(text)
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name] = ast.get_source_segment(text, node) or ''
    return out


class V2DiffProof(unittest.TestCase):
    """v2 is v1 plus a declared list of hunks, and the list is proved, not asserted."""

    DECLARED = ('PARTIAL_UNRESOLVED', 'partial_unresolved', 'dispatch_scope',
                'scoped_endpoints', 'scoped_arms', 'planned_call_count',
                'all_coordinates', 'plan_body', '_offline_preflight',
                'decode_contribution', 'validate_material')

    def test_v1_is_the_published_driver_and_is_not_edited_by_this_fork(self):
        self.assertEqual(V1_SOURCE.name, 'contrast_triple_study.py')
        self.assertEqual(V2_SOURCE.name, 'contrast_triple_study_v2.py')
        self.assertNotEqual(V1_SOURCE.resolve(), V2_SOURCE.resolve())
        published = hashlib.sha256(V1_SOURCE.read_bytes()).hexdigest()
        # The v2 header cites the bytes it copied; if v1 moves, the citation is stale and
        # this fails rather than quietly describing a file that no longer exists.
        self.assertIn(published, c.__doc__)

    def test_every_differing_line_is_marked_V2(self):
        import difflib
        old, new = _normalised(V1_SOURCE), _normalised(V2_SOURCE)
        matcher = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
        hunks = [op for op in matcher.get_opcodes() if op[0] != 'equal']
        self.assertTrue(hunks, 'v2 is byte-identical to v1 outside the docstring')
        for tag, i1, i2, j1, j2 in hunks:
            # The marker may sit on a changed line or on the comment block immediately
            # above it inside the same definition, so the window is the hunk plus the
            # eight lines of new source that precede it. A hunk with no marker anywhere
            # in that window is an undeclared change.
            block = old[i1:i2] + new[max(0, j1 - 8):j2]
            self.assertTrue(any('V2:' in line for line in block),
                            'unmarked hunk: ' + repr((old[i1:i2] + new[j1:j2])[:6]))

    def test_only_the_declared_definitions_differ(self):
        old, new = _definitions(V1_SOURCE), _definitions(V2_SOURCE)
        added = sorted(set(new) - set(old))
        removed = sorted(set(old) - set(new))
        changed = sorted(name for name in set(old) & set(new) if old[name] != new[name])
        self.assertEqual(added, ['partial_unresolved', 'planned_call_count',
                                 'scoped_arms', 'scoped_endpoints'])
        self.assertEqual(removed, [])
        self.assertEqual(changed, ['_offline_preflight', 'all_coordinates',
                                   'decode_contribution', 'plan_body', 'validate_material'])
        for name in added + changed:
            self.assertIn(name, self.DECLARED)

    def test_v2_writes_its_own_digest_as_helper_sha256(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'occ'
            c.prepare(MATERIAL_V2, out, REPO)
            plan = json.loads((out / 'plan.json').read_bytes())
        self.assertEqual(plan['helper_sha256'],
                         hashlib.sha256(V2_SOURCE.read_bytes()).hexdigest())
        self.assertNotEqual(plan['helper_sha256'],
                            hashlib.sha256(V1_SOURCE.read_bytes()).hexdigest())

    def test_the_published_occurrence_01_plan_is_untouched_by_this_fork(self):
        published = REPO / 'experiments/diagnostics/C001-contrast-triple/occurrence-01/plan.json'
        if not published.exists():
            self.skipTest('occurrence-01 is not present in this tree')
        plan = json.loads(published.read_bytes())
        self.assertEqual(plan['helper_sha256'],
                         hashlib.sha256(V1_SOURCE.read_bytes()).hexdigest())
        self.assertEqual(plan['planned_calls'], 240)
        self.assertNotIn('dispatch_scope', plan)
        self.assertEqual(plan['ceilings']['max_tokens']['deepseek-flash'], 8192)


class V1Parity(unittest.TestCase):
    """On a material that declares no scope, v2 is v1 but for its own digest."""

    def test_plan_bodies_agree_on_every_field_except_helper_sha256(self):
        raw = MATERIAL.read_bytes()
        one = v1.plan_body(v1.validate_material(json.loads(raw)), raw, V1_SOURCE.read_bytes())
        two = c.plan_body(c.validate_material(json.loads(raw)), raw, V2_SOURCE.read_bytes())
        differing = sorted(k for k in set(one) | set(two) if one.get(k) != two.get(k))
        self.assertEqual(differing, ['helper_sha256'])

    def test_an_unscoped_material_plans_the_full_240(self):
        data = material()
        self.assertIsNone(data.get('dispatch_scope'))
        self.assertEqual(c.planned_call_count(data), c.PLANNED_CALLS)
        self.assertEqual(c.planned_call_count(data), 240)
        self.assertEqual(c.all_coordinates(data), v1.all_coordinates(data))
        self.assertEqual(len(c.scoped_endpoints(data)), 6)
        self.assertEqual(c.scoped_arms(data), c.ARMS)

    def test_an_unscoped_plan_carries_no_dispatch_scope_key(self):
        raw = MATERIAL.read_bytes()
        body = c.plan_body(c.validate_material(json.loads(raw)), raw, V2_SOURCE.read_bytes())
        self.assertNotIn('dispatch_scope', body)


class DispatchScope(unittest.TestCase):
    """The scope narrows dispatch, is validated, and is inside the identity."""

    def test_the_occurrence_02_material_scopes_one_endpoint_and_one_arm(self):
        data = material_v2()
        scope = data['dispatch_scope']
        self.assertEqual(scope['endpoints'], ['deepseek-flash'])
        self.assertEqual(scope['arms'], ['fcl'])
        self.assertTrue(scope['reason'].strip())
        self.assertEqual(c.planned_call_count(data), 20)
        self.assertEqual(data['planned_calls'], 20)

    def test_the_coordinates_are_the_v1_list_with_the_others_removed(self):
        data = material_v2()
        scoped = c.all_coordinates(data)
        full = [coord for coord in v1.all_coordinates(data)
                if coord['endpoint_slug'] == 'deepseek-flash' and coord['arm'] == 'fcl']
        self.assertEqual(scoped, full)
        self.assertEqual(len(scoped), 20)
        self.assertEqual(sorted({coord['case'] for coord in scoped}), sorted(c.CASES))
        self.assertEqual(sorted({coord['replicate'] for coord in scoped}), [1, 2, 3, 4, 5])

    def test_the_scope_is_frozen_into_the_plan_and_into_plan_id(self):
        raw = MATERIAL_V2.read_bytes()
        data = c.validate_material(json.loads(raw))
        body = c.plan_body(data, raw, V2_SOURCE.read_bytes())
        self.assertEqual(body['dispatch_scope'], data['dispatch_scope'])
        self.assertEqual(body['planned_calls'], 20)
        widened = json.loads(raw)
        widened['dispatch_scope']['arms'] = ['fcl', 'prose']
        widened['planned_calls'] = 40
        other = c.plan_body(c.validate_material(widened), json.dumps(widened).encode(),
                            V2_SOURCE.read_bytes())
        self.assertNotEqual(c.digest(body), c.digest(other))

    def test_twenty_coordinates_make_four_single_key_waves(self):
        raw = MATERIAL_V2.read_bytes()
        body = c.plan_body(c.validate_material(json.loads(raw)), raw, V2_SOURCE.read_bytes())
        body['plan_id'] = c.digest(body)
        waves = c.build_waves(body)
        self.assertEqual(len(waves), 4)
        for wave in waves:
            self.assertEqual(len(wave['coordinates']), 5)
            self.assertEqual({coord['endpoint_slug'] for coord in wave['coordinates']},
                             {'deepseek-flash'})

    def test_a_malformed_scope_is_refused(self):
        raw = json.loads(MATERIAL_V2.read_bytes())
        for mutate, code in (
                (lambda d: d.__setitem__('dispatch_scope', []), 'MATERIAL_DISPATCH_SCOPE'),
                (lambda d: d['dispatch_scope'].pop('reason'), 'MATERIAL_DISPATCH_SCOPE'),
                (lambda d: d['dispatch_scope'].__setitem__('reason', '  '),
                 'MATERIAL_DISPATCH_SCOPE'),
                (lambda d: d['dispatch_scope'].__setitem__('extra', 1),
                 'MATERIAL_DISPATCH_SCOPE'),
                (lambda d: d['dispatch_scope'].__setitem__('endpoints', []),
                 'MATERIAL_DISPATCH_SCOPE_ENDPOINTS'),
                (lambda d: d['dispatch_scope'].__setitem__('endpoints', ['nope']),
                 'MATERIAL_DISPATCH_SCOPE_ENDPOINTS'),
                (lambda d: d['dispatch_scope'].__setitem__(
                    'endpoints', ['deepseek-flash', 'deepseek-flash']),
                 'MATERIAL_DISPATCH_SCOPE_ENDPOINTS'),
                (lambda d: d['dispatch_scope'].__setitem__('arms', []),
                 'MATERIAL_DISPATCH_SCOPE_ARMS'),
                (lambda d: d['dispatch_scope'].__setitem__('arms', ['nope']),
                 'MATERIAL_DISPATCH_SCOPE_ARMS'),
                (lambda d: d['dispatch_scope'].__setitem__('arms', ['fcl', 'fcl']),
                 'MATERIAL_DISPATCH_SCOPE_ARMS')):
            data = json.loads(json.dumps(raw))
            mutate(data)
            with self.assertRaises(ValueError) as caught:
                c.validate_material(data)
            self.assertEqual(str(caught.exception), code)

    def test_a_planned_calls_that_disagrees_with_the_scope_is_refused(self):
        data = json.loads(MATERIAL_V2.read_bytes())
        data['planned_calls'] = 240
        with self.assertRaises(ValueError) as caught:
            c.validate_material(data)
        self.assertEqual(str(caught.exception), 'MATERIAL_PLANNED_CALLS')

    def test_v1_silently_widens_this_material_to_240_which_is_the_hazard(self):
        """v1 does not REFUSE the occurrence-02 material -- it silently ignores the scope.

        This is the finding that makes the successor identity necessary rather than
        merely tidy. v1 has no notion of `dispatch_scope` and does not read the
        material's own `planned_calls`, so given the occurrence-02 material it plans the
        full 240 coordinates -- all six endpoints, both arms -- at the raised 32768
        ceiling, twelve times the twenty calls the material declares and the receipt
        authorises. Nothing in v1 stops it. The preflight check the publisher must run
        before dispatch is therefore `planned_calls == 20`, and it must be run against a
        plan built by v2.
        """
        raw = MATERIAL_V2.read_bytes()
        body = v1.plan_body(v1.validate_material(json.loads(raw)), raw, V1_SOURCE.read_bytes())
        self.assertEqual(body['planned_calls'], 240)
        self.assertEqual(len(body['coordinates']), 240)
        self.assertNotIn('dispatch_scope', body)
        self.assertEqual(json.loads(raw)['planned_calls'], 20)
        # v2 on the same bytes plans exactly what the material declares.
        mine = c.plan_body(c.validate_material(json.loads(raw)), raw, V2_SOURCE.read_bytes())
        self.assertEqual(mine['planned_calls'], 20)
        self.assertEqual(len(mine['coordinates']), 20)


class Occurrence02Material(unittest.TestCase):
    """The raised ceiling, the raised timeout, and everything else carried through."""

    def test_deepseek_carries_the_authorised_maximum_and_the_transport_maximum(self):
        data = material_v2()
        entry = next(e for e in data['endpoints'] if e['id'] == 'deepseek-flash')
        self.assertEqual(entry['max_tokens'], 32768)
        self.assertEqual(entry['max_tokens'], c.MAX_TOKENS_AUTHORISED)
        self.assertEqual(entry['timeout_seconds'], 600)
        self.assertEqual(entry['timeout_seconds'], c.TIMEOUT_SECONDS_AUTHORISED)
        self.assertEqual(data['ceilings']['max_tokens']['deepseek-flash'], 32768)
        self.assertEqual(data['ceilings']['timeout_seconds']['deepseek-flash'], 600)

    def test_601_seconds_is_refused_by_the_transport_itself(self):
        from minireason.provider_openai_compat import ENDPOINTS
        base = ENDPOINTS['deepseek-flash']
        dataclasses.replace(base, timeout_seconds=600)
        with self.assertRaises(Exception):
            dataclasses.replace(base, timeout_seconds=601)

    def test_every_other_endpoint_is_the_published_entry_unchanged(self):
        published = {e['id']: e for e in material()['endpoints']}
        for entry in material_v2()['endpoints']:
            if entry['id'] == 'deepseek-flash':
                continue
            self.assertEqual(entry, published[entry['id']])

    def test_the_prompts_the_recoding_and_the_reading_rule_are_carried_through(self):
        one, two = material(), material_v2()
        for field in ('arms', 'cases', 'replicates', 'seeds', 'seed_policy', 'node',
                      'reading_rule', 'question', 'claim_ceiling', 'system_common',
                      'public_contract', 'envelope', 'envelope_unwrap', 'policies',
                      'problem', 'render', 'source_pins', 'transport_pins', 'study'):
            self.assertEqual(one[field], two[field], field)

    def test_the_briefs_and_the_recoding_table_are_occurrence_01s_bytes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            one = Path(tmp) / 'one'
            two = Path(tmp) / 'two'
            c.prepare(MATERIAL, one, REPO)
            c.prepare(MATERIAL_V2, two, REPO)
            self.assertEqual((one / 'RECODING_TABLE.md').read_bytes(),
                             (two / 'RECODING_TABLE.md').read_bytes())
            for arm in c.ARMS:
                for case in c.CASES:
                    a = json.loads((one / 'briefs' / arm / (case + '.json')).read_bytes())
                    b = json.loads((two / 'briefs' / arm / (case + '.json')).read_bytes())
                    self.assertEqual(a['messages'], b['messages'])
                    self.assertEqual(a['messages_sha256'], b['messages_sha256'])
                    self.assertEqual(a['brief_sha256'], b['brief_sha256'])
                    self.assertNotEqual(a['plan_id'], b['plan_id'])
            one_plan = json.loads((one / 'plan.json').read_bytes())
            two_plan = json.loads((two / 'plan.json').read_bytes())
            self.assertEqual(one_plan['briefs'], two_plan['briefs'])

    def test_prepare_plans_twenty_and_spends_nothing(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'occ'
            result = c.prepare(MATERIAL_V2, out, REPO)
            self.assertEqual(result['planned_calls'], 20)
            self.assertEqual(result['provider_calls'], 0)
            preflight = json.loads((out / 'preflight.json').read_bytes())
            self.assertEqual(preflight['status'], 'OFFLINE_PREFLIGHT_PASSED')
            self.assertEqual(preflight['payloads_built_by_the_transport'], 20)
            self.assertEqual(preflight['provider_calls'], 0)
            self.assertEqual(preflight['distinct_message_pairs'], 4)
            _, plan = c.verify(out, REPO)
            self.assertEqual(plan['plan_id'], result['plan_id'])

    def test_every_built_payload_carries_the_raised_ceiling(self):
        data = material_v2()
        endpoints = {e['slug']: e for e in data['endpoints']}
        for coord in c.all_coordinates(data):
            spec = c.spec_for(endpoints[coord['endpoint_slug']], coord)
            self.assertEqual(spec['max_tokens'], 32768)
            self.assertEqual(spec['timeout_seconds'], 600)

    def test_the_material_states_the_evidence_and_claims_no_rescue(self):
        policy = material_v2()['ceilings']['max_tokens_policy']
        for fragment in ('COMPLETE 21 / PARTIAL 8 / FAILED 11', 'NO_PUBLIC_CONTENT',
                         'reasoning_content_present true', 'is NOT predicted to be sufficient',
                         'NO OCCURRENCE-01 RECORD IS MODIFIED',
                         'new budget conditions require separate freezing'):
            self.assertIn(fragment, policy)
        timeout = material_v2()['ceilings']['timeout_seconds_policy']
        for fragment in ('tokens per second', '215', 'REC-20260914-T'):
            self.assertIn(fragment, timeout)

    def test_the_partial_rule_no_longer_names_8192_as_an_endpoints_ceiling(self):
        rule = material_v2()['partial_delivery_rule']
        self.assertIn('32768 for every endpoint of this material', rule)
        self.assertNotIn('8192 for deepseek-flash', rule)


class PartialUnresolvedNamesItsOwnCeiling(unittest.TestCase):
    """A PARTIAL receipt states the ceiling the call actually ran under."""

    def test_the_reason_is_built_from_the_specs_own_ceiling(self):
        self.assertIn('32768-token ceiling', c.partial_unresolved(32768))
        self.assertIn('8192-token ceiling', c.partial_unresolved(8192))
        self.assertIn('FW5:634', c.partial_unresolved(32768))

    def test_v1_would_have_named_8192_on_a_32768_partial(self):
        self.assertIn('8192-token ceiling', v1.PARTIAL_UNRESOLVED)
        self.assertNotEqual(v1.PARTIAL_UNRESOLVED, c.partial_unresolved(32768))
        self.assertEqual(v1.PARTIAL_UNRESOLVED, c.partial_unresolved(8192))

    def test_an_out_of_range_ceiling_is_refused(self):
        for bad in (0, -1, 32769, '8192', None, 8192.0):
            with self.assertRaises(ValueError):
                c.partial_unresolved(bad)

    def test_a_partial_delivery_records_the_raised_ceiling(self):
        payload = {'model': 'm', 'messages': [{'role': 'user', 'content': 'x'}],
                   'max_tokens': 32768, 'response_format': {'type': 'json_object'},
                   'seed': 1, 'stream': False}
        spec = {'max_tokens': 32768, 'timeout_seconds': 600}
        record = {'request': payload, 'request_sha256': c.digest(payload),
                  'content': json.dumps({'body': 'b', 'commitments': 'c'}),
                  'status': 'INCOMPLETE_GENERATION', 'finish_reason': 'length',
                  'usage': {'prompt_tokens': 1, 'completion_tokens': 32768}}
        out = c.decode_contribution(record, payload, spec)
        self.assertEqual(out['delivery_status'], 'PARTIAL')
        self.assertFalse(out['comparable'])
        self.assertIn('32768-token ceiling', out['unresolved_reason'])
        self.assertNotIn('8192', out['unresolved_reason'])


class ScopedDispatch(unittest.TestCase):
    """The whole occurrence end to end, offline: twenty calls, four waves, clean audit."""

    @staticmethod
    def _prepared(tmp: Path):
        out = tmp / 'occ'
        return out, c.prepare(MATERIAL_V2, out, REPO)

    def test_twenty_calls_four_waves_and_an_audit_that_ties_to_the_plan(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = self._prepared(Path(tmp))
            ScriptedProvider.reset()
            summary = c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                            notify=lambda message: None)
            self.assertEqual(summary['planned_calls'], 20)
            self.assertEqual(summary['dispatched'], 20)
            self.assertEqual(summary['waves'], 4)
            self.assertEqual(ScriptedProvider.peak.get('DEEPSEEK_API_KEY', 0),
                             c.MAX_CONCURRENT_PER_KEY)
            self.assertNotIn('OLLAMA_API_KEY', ScriptedProvider.peak)
            report = c.audit(out, REPO)
            self.assertEqual(report['planned_calls'], 20)
            self.assertEqual(report['counts']['COMPLETE'], 20)
            self.assertEqual(report['counts']['not_dispatched'], 0)
            self.assertEqual(report['counts']['unresolved_attempts'], 0)
            self.assertEqual(sorted(report['seed_by_endpoint']), ['deepseek-flash'])

    def test_no_out_of_scope_coordinate_is_written_anywhere(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = self._prepared(Path(tmp))
            ScriptedProvider.reset()
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda message: None)
            for category in ('requests', 'attempts', 'responses', 'artifacts', 'provider'):
                written = sorted(path.relative_to(out / category).parts[:2]
                                 for path in (out / category).rglob('*')
                                 if path.is_file())
                self.assertTrue(written)
                self.assertEqual({parts[0] for parts in written}, {'deepseek-flash'})
                self.assertEqual({parts[1] for parts in written}, {'fcl'})
            self.assertFalse((out / 'responses' / 'ollama-glm-5.3').exists())

    def test_a_partial_at_the_raised_ceiling_names_32768_in_its_receipt(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = self._prepared(Path(tmp))
            label = 'deepseek-flash/fcl/original/rep1'
            replies = {label: {
                'status': 'INCOMPLETE_GENERATION', 'finish_reason': 'length',
                'content': json.dumps({'body': 'truncated', 'commitments': ''}),
                'usage': {'prompt_tokens': 11, 'completion_tokens': 32768,
                          'total_tokens': 32779},
                'reasoning_content_present': True}}
            ScriptedProvider.reset(replies=replies)
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda message: None)
            receipt = json.loads(
                (out / 'responses/deepseek-flash/fcl/original/rep1.json').read_bytes())
            self.assertEqual(receipt['status'], 'PARTIAL')
            self.assertFalse(receipt['comparable'])
            self.assertEqual(receipt['timeout_seconds'], 600)
            self.assertIn('32768-token ceiling', receipt['unresolved_reason'])
            self.assertNotIn('8192', receipt['unresolved_reason'])
            report = c.audit(out, REPO)
            self.assertEqual(report['counts']['PARTIAL'], 1)
            self.assertEqual(report['counts']['unresolved_partial'], 1)

    def test_every_request_record_carries_32768_and_600(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = self._prepared(Path(tmp))
            ScriptedProvider.reset()
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda message: None)
            requests = sorted((out / 'requests').rglob('rep*.json'))
            self.assertEqual(len(requests), 20)
            for path in requests:
                request = json.loads(path.read_bytes())
                self.assertEqual(request['spec']['max_tokens'], 32768)
                self.assertEqual(request['provider_payload']['max_tokens'], 32768)
                self.assertEqual(request['spec']['timeout_seconds'], 600)
                self.assertEqual(request['timeout_seconds'], 600)
                self.assertEqual(request['plan_id'], result['plan_id'])

    def test_the_table_renders_one_cell_and_leaves_roots_columns_empty(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out, result = self._prepared(Path(tmp))
            ScriptedProvider.reset(replies=Comparison._replies())
            c.run(out, result['plan_id'], REPO, provider_factory=ScriptedProvider,
                  notify=lambda message: None)
            rendered = c.table(out, REPO)
            self.assertEqual(rendered['tables'], 1)
            data = json.loads((out / 'comparison.json').read_bytes())
            self.assertEqual(len(data['tables']), 1)
            self.assertEqual(data['tables'][0]['endpoint_slug'], 'deepseek-flash')
            self.assertEqual(data['tables'][0]['arm'], 'fcl')
            for value in data['tables'][0]['root_reading'].values():
                self.assertEqual(value, '')
            c.assert_no_scoring_keys(data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
