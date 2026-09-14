"""H005: immutable outer DAG fixture using canonical Mini artifacts and rendering.

No durable scheduler, semantic validator, automatic retry, or Git mutation is used.
Each cycle is a complete template invocation; nodes are individual model calls.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import getpass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / 'src'))
sys.path.insert(0, str(REPOSITORY))
from creib.forge.mini.kinds import Submission, read_submission
from creib.forge.mini.log import ARTIFACT_SUBMITTED, MiniState, apply_event, build_event
from creib.forge.mini.manifest import Stage, compile_manifest
from creib.forge.mini.runner import _store_artifact, render_brief
from minireason.provider import DeepSeek, Settings, digest
from tools.multicycle_language_probe import MemoryBlobs

ARMS = ('bare', 'native', 'matched', 'mini_prose', 'mini_fcl')
BASELINE_ARMS = ('bare', 'native')
CAP = 8192
VIEWS = ('body', 'commitments', 'both')
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z')
ENVELOPE = ('## What to return\nA JSON object carrying "body" and "commitments". '
            'Both are strings and nothing else is required.')
PUBLIC_CONTRACT = ('Return one JSON object with exactly two string fields: "body" and '
                   '"commitments". Write the actual commitments separately; do not copy '
                   'the body into that field as a storage shortcut.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def load(path):
    return json.loads(Path(path).read_bytes())


def utc():
    return datetime.now(timezone.utc).isoformat()


def write_new(path, value):
    raw = value if isinstance(value, bytes) else encoded(value)
    key = os.environ.get('DEEPSEEK_API_KEY')
    if key and key.encode('utf-8') in raw:
        raise ValueError('CREDENTIAL_IN_OUTPUT')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError('INVALID_IDENTIFIER')
    return value


def settings_for(arm):
    if arm not in ARMS:
        raise ValueError('UNKNOWN_ARM')
    return Settings(thinking=arm == 'native', reasoning_effort='low',
                    max_tokens=CAP, timeout_seconds=180)


def payload_for(messages, settings):
    payload = {'model': settings.model, 'messages': messages, 'stream': False,
               'max_tokens': settings.max_tokens,
               'thinking': {'type': 'enabled' if settings.thinking else 'disabled'},
               'response_format': {'type': 'json_object'}}
    if settings.thinking:
        payload['reasoning_effort'] = settings.reasoning_effort
    return payload


def safe_source(repo, name):
    path = Path(name)
    resolved = (Path(repo) / path).resolve()
    if path.is_absolute() or '..' in path.parts or not resolved.is_relative_to(Path(repo).resolve()):
        raise ValueError('SOURCE_PIN_OUTSIDE_REPOSITORY')
    return resolved


def validate_material(material):
    if material.get('schema') != 'minireason.h005.material.v1':
        raise ValueError('MATERIAL_SCHEMA')
    for name in ('system', 'prose_instruction', 'formal_instruction', 'bare_instruction'):
        if not isinstance(material.get(name), str):
            raise ValueError('MATERIAL_TEXT')
    templates = material.get('templates')
    if not isinstance(templates, dict) or not templates:
        raise ValueError('MATERIAL_TEMPLATES')
    for tid, template in templates.items():
        identifier(tid)
        nodes = template.get('nodes')
        if not isinstance(nodes, list) or not nodes:
            raise ValueError('TEMPLATE_NODES')
        seen = set()
        for node in nodes:
            nid = identifier(node['id'])
            if nid in seen or nid in ('previous', 'origin', 'task', 'end'):
                raise ValueError('DUPLICATE_OR_RESERVED_NODE')
            if not isinstance(node.get('instruction'), str) or not isinstance(node.get('inputs'), list):
                raise ValueError('NODE_FIELDS')
            for binding in node['inputs']:
                if (set(binding) != {'source', 'view'} or binding['view'] not in VIEWS
                        or binding['source'] not in seen | {'previous', 'origin'}):
                    raise ValueError('NON_ACYCLIC_OR_INVALID_INPUT')
            seen.add(nid)
    problems = material.get('problems')
    if not isinstance(problems, list) or not problems:
        raise ValueError('MATERIAL_PROBLEMS')
    seen = set()
    for problem in problems:
        pid = identifier(problem['id'])
        chain = problem.get('templates')
        if pid in seen or not isinstance(problem.get('prose'), str):
            raise ValueError('PROBLEM_FIELDS')
        if not isinstance(chain, list) or not 3 <= len(chain) <= 5 or any(t not in templates for t in chain):
            raise ValueError('TEMPLATE_CHAIN')
        seen.add(pid)
    if not isinstance(material.get('source_pins', {}), dict):
        raise ValueError('SOURCE_PINS')
    return material


def kind(identity, title, ports, instruction='Use only the declared inputs.'):
    return {'kind_id': identity, 'title': title, 'instruction': instruction,
            'commitment_call': 'single', 'input_ports': ports,
            'output_port': {'port_id': 'out', 'produces_kind': identity},
            'failure_policy': {'retries': 0, 'tolerance': 0, 'action': 'stop'}}


def projection_id(node_id, index):
    return f'p.{node_id}.{index}'


def manifest_for(tid, template):
    task = 'h005.task.v1'
    kinds = [kind(task, 'Original problem', [])]
    stages = [{'stage_id': 'task', 'kind_id': task, 'seat': 'machine', 'ports': []}]
    port_types = [{'port_type': 'task', 'draws_from': {'artifact_kinds': [task]},
                   'render': {'rule': 'list_bodies', 'header': 'Original problem'}}]
    nodes = template['nodes']
    for index, node in enumerate(nodes):
        ports = [{'port_id': 'task', 'port_type': 'task', 'window': 'this_cycle'}]
        for i, binding in enumerate(node['inputs']):
            proj = projection_id(node['id'], i)
            identity = f'h005.{tid}.{proj}'
            kinds.append(kind(identity, 'Explicit field projection', []))
            stages.append({'stage_id': proj, 'kind_id': identity, 'seat': 'machine', 'ports': []})
            port_types.append({'port_type': proj, 'draws_from': {'artifact_kinds': [identity]},
                               'render': {'rule': 'list_bodies', 'header': 'Selected input ' + binding['source']}})
            ports.append({'port_id': proj, 'port_type': proj, 'window': 'this_cycle'})
        identity = 'mini.verdict.v1' if index == len(nodes) - 1 else f'h005.{tid}.{node["id"]}'
        kinds.append(kind(identity, node['id'], ports, node['instruction']))
        stages.append({'stage_id': node['id'], 'kind_id': identity,
                       'ports': [port['port_id'] for port in ports]})
    stages.append({'stage_id': 'end', 'end': True})
    return {'schema_version': 'creib.mini.manifest.v1', 'manifest_id': 'h005.' + tid,
            'problem': 'One arbitrary template invocation in H005.',
            'cycles': {'max_cycles': 1, 'max_calls': len(nodes),
                       'completion_tokens_per_call': CAP, 'max_completion_tokens': len(nodes) * CAP},
            'kinds': kinds, 'port_types': port_types, 'stages': stages}


def runtime_pins(repo):
    repo = Path(repo)
    paths = list((repo / 'src' / 'creib').rglob('*.py'))
    paths += [repo / 'src/minireason/provider.py', repo / 'tools/multicycle_language_probe.py']
    return {p.relative_to(repo).as_posix(): sha(p.read_bytes()) for p in sorted(paths)}


def plan_body(repo, raw, material):
    for name, expected in material.get('source_pins', {}).items():
        if sha(safe_source(repo, name).read_bytes()) != expected:
            raise ValueError('SOURCE_PIN_MISMATCH')
    return {'schema': 'minireason.h005.plan.v1', 'material_sha256': sha(raw),
            'helper_sha256': sha(Path(__file__).read_bytes()), 'runtime_pins': runtime_pins(repo),
            'source_pins': material.get('source_pins', {}), 'arms': list(ARMS),
            'settings': {arm: settings_for(arm).to_dict() for arm in ARMS},
            'max_concurrent_requests': 5, 'automatic_retries': 0,
            'cycle_definition': 'one complete template invocation',
            'formal_syntax_validation': False,
            'partial_public_continuation': True,
            'max_calls': sum(2 + 3 * len(material['templates'][tid]['nodes'])
                             for p in material['problems'] for tid in p['templates']),
            'manifests': {tid: sha(encoded(manifest_for(tid, template)))
                          for tid, template in material['templates'].items()}}


def initialize(repo, output, material_path):
    output = Path(output)
    raw = Path(material_path).read_bytes()
    material = validate_material(json.loads(raw))
    plan = plan_body(repo, raw, material)
    plan['plan_id'] = digest(plan)
    with tempfile.TemporaryDirectory(prefix='h005-compile-') as temporary:
        for tid, template in material['templates'].items():
            path = Path(temporary) / (tid + '.json')
            write_new(path, manifest_for(tid, template))
            compile_manifest(path)
    if output.exists():
        existing = list(output.iterdir())
        if any(p.name != 'material.json' for p in existing):
            raise ValueError('OCCURRENCE_EXISTS')
        if (output / 'material.json').exists() and (output / 'material.json').read_bytes() != raw:
            raise ValueError('MATERIAL_EXISTS_DIFFERENT')
    if not (output / 'material.json').exists():
        write_new(output / 'material.json', raw)
    for tid, template in material['templates'].items():
        write_new(output / 'manifests' / (tid + '.json'), manifest_for(tid, template))
    write_new(output / 'plan.json', plan)
    return plan


def verify(repo, output):
    output = Path(output)
    raw = (output / 'material.json').read_bytes()
    material = validate_material(json.loads(raw))
    expected = plan_body(repo, raw, material)
    expected['plan_id'] = digest(expected)
    if load(output / 'plan.json') != expected:
        raise ValueError('IMMUTABLE_PLAN_MISMATCH')
    for tid, expected_hash in expected['manifests'].items():
        if sha((output / 'manifests' / (tid + '.json')).read_bytes()) != expected_hash:
            raise ValueError('MANIFEST_PIN_MISMATCH')
    return material, expected

def problem_for(material, problem_id):
    identifier(problem_id)
    for problem in material['problems']:
        if problem['id'] == problem_id:
            return problem
    raise ValueError('UNKNOWN_PROBLEM')


def coordinate(problem, arm, cycle, node):
    return {'problem': problem, 'arm': arm, 'cycle': cycle, 'node': node}


def label(coord):
    return f'{coord["problem"]}/{coord["arm"]}/cycle-{coord["cycle"]}/{coord["node"]}'


def at(output, category, coord, suffix='json'):
    for name in ('problem', 'arm', 'node'):
        identifier(coord[name])
    if coord['arm'] not in ARMS or type(coord['cycle']) is not int or not 1 <= coord['cycle'] <= 5:
        raise ValueError('INVALID_COORDINATE')
    identifier(category)
    identifier(suffix)
    return (Path(output) / category / coord['problem'] / coord['arm'] /
            f'cycle{coord["cycle"]:02d}' / (coord['node'] + '.' + suffix))


def provider_dir(output, coord):
    return at(output, 'provider', coord).with_suffix('')


def nodes_for(material, problem, arm, cycle):
    if arm not in ARMS or type(cycle) is not int or not 1 <= cycle <= len(problem['templates']):
        raise ValueError('INVALID_TEMPLATE_COORDINATE')
    if arm in BASELINE_ARMS:
        return [{'id': 'answer', 'instruction': material['bare_instruction'], 'inputs': []}]
    return material['templates'][problem['templates'][cycle - 1]]['nodes']


def final_coordinate(material, problem, arm, cycle):
    return coordinate(problem['id'], arm, cycle, nodes_for(material, problem, arm, cycle)[-1]['id'])


def source_coordinate(material, problem, coord, source):
    if source in ('previous', 'origin'):
        if coord['cycle'] == 1:
            return None
        return final_coordinate(material, problem, coord['arm'],
                                coord['cycle'] - 1 if source == 'previous' else 1)
    return coordinate(coord['problem'], coord['arm'], coord['cycle'], source)


def decode_contribution(record, payload, settings):
    if (record.get('request') != payload or record.get('request_sha256') != digest(payload)
            or record.get('settings') != settings.to_dict()):
        raise ValueError('PROVIDER_REQUEST_CUSTODY')
    content, usage = record.get('content'), record.get('usage')
    if not isinstance(content, str) or not content.strip():
        raise ValueError('NO_PUBLIC_CONTENT')
    if not isinstance(usage, dict) or any(type(usage.get(k)) is not int or usage[k] < 0
                                        for k in ('prompt_tokens', 'completion_tokens', 'total_tokens')):
        raise ValueError('PROVIDER_USAGE_INVALID')
    if usage['completion_tokens'] > CAP:
        raise ValueError('PROVIDER_CAP_EXCEEDED')
    if (record.get('reasoning_content_persisted') or record.get('credential_redaction')
            or (record.get('reasoning_content_present') and not settings.thinking)):
        raise ValueError('PROVIDER_CONTENT_CUSTODY')
    pair = (record.get('status'), record.get('finish_reason'))
    if pair == ('COMPLETE', 'stop'):
        delivery = 'COMPLETE'
    elif pair == ('INCOMPLETE_GENERATION', 'length'):
        delivery = 'PARTIAL'
    else:
        raise ValueError('PROVIDER_NOT_USABLE')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('DUPLICATE_JSON_FIELD')
            result[key] = value
        return result
    try:
        envelope = json.loads(content, object_pairs_hook=unique)
        valid = (isinstance(envelope, dict) and set(envelope) == {'body', 'commitments'}
                 and all(isinstance(v, str) for v in envelope.values()))
    except (ValueError, TypeError):
        valid = False
    body = envelope['body'] if valid else content
    commitments = envelope['commitments'] if valid else ''
    return {'body': body, 'commitments': commitments, 'delivery_status': delivery,
            'envelope_status': 'AUTHORED' if valid else 'OPAQUE',
            'public_text_sha256': sha(content.encode('utf-8')),
            'body_sha256': sha(body.encode('utf-8')),
            'commitments_sha256': sha(commitments.encode('utf-8'))}


def authored_artifact(coord, contribution):
    blobs = MemoryBlobs()
    stage = Stage(label(coord), 'h005.authored.v1', (), False)
    submission = Submission(contribution['body'], contribution['commitments'], (), (), (), {})
    aid, body_ref, commitment_ref = _store_artifact(blobs, stage, submission, 0)
    return {'schema': 'minireason.h005.artifact.v1', 'coordinate': coord,
            'artifact_id': aid, 'body_ref': body_ref, 'commitments_ref': commitment_ref,
            **contribution}


def read_terminal(output, coord):
    request = load(at(output, 'requests', coord))
    trace = load(at(output, 'traces', coord))
    attempt = load(at(output, 'attempts', coord))
    receipt = load(at(output, 'responses', coord))
    settings = settings_for(coord['arm'])
    payload = payload_for(request['messages'], settings)
    if (any(v.get('coordinate') != coord for v in (request, trace, attempt, receipt))
            or request['trace_sha256'] != digest(trace)
            or request['messages_sha256'] != digest(request['messages'])
            or request['provider_payload'] != payload
            or request['settings'] != settings.to_dict()
            or attempt['request_sha256'] != digest(request)
            or receipt['request_sha256'] != digest(request)):
        raise ValueError('TERMINAL_CUSTODY_MISMATCH')
    response_path = provider_dir(output, coord) / 'call-0001.response.json'
    request_path = provider_dir(output, coord) / 'call-0001.request.json'
    for path, field in ((response_path, 'provider_response_sha256'), (request_path, 'provider_request_sha256')):
        actual = sha(path.read_bytes()) if path.exists() else None
        if actual != receipt.get(field):
            raise ValueError('PROVIDER_BYTES_CHANGED')
    if receipt['status'] in ('COMPLETE', 'PARTIAL'):
        record = load(response_path)
        provider_request = load(request_path)
        if (provider_request.get('request') != payload
                or provider_request.get('request_sha256') != digest(payload)
                or provider_request.get('settings') != settings.to_dict()
                or provider_request.get('coordinate') != {'harness': 'H005', **coord}
                or record.get('coordinate') != {'harness': 'H005', **coord}):
            raise ValueError('PROVIDER_REQUEST_FILE_CHANGED')
        contribution = decode_contribution(record, payload, settings)
        artifact = authored_artifact(coord, contribution)
        artifact_path = at(output, 'artifacts', coord)
        if (load(artifact_path) != artifact or sha(artifact_path.read_bytes()) != receipt['artifact_sha256']
                or at(output, 'responses', coord, 'txt').read_bytes() != record['content'].encode('utf-8')
                or receipt['status'] != contribution['delivery_status']
                or receipt['envelope_status'] != contribution['envelope_status']
                or receipt['usage'] != record['usage']):
            raise ValueError('ARTIFACT_CUSTODY_MISMATCH')
    elif receipt['status'] != 'FAILED':
        raise ValueError('TERMINAL_STATUS_INVALID')
    return receipt


def read_artifact(output, coord):
    if read_terminal(output, coord)['status'] not in ('COMPLETE', 'PARTIAL'):
        raise ValueError('SOURCE_NOT_USABLE')
    return load(at(output, 'artifacts', coord))


def project(source, view, artifact, previous_coord):
    if artifact is None:
        return ('Source ' + source + ': absent in the first template invocation; selected view ' + view + '.',
                {'source': source, 'view': view, 'absent': True})
    trace = {'source': source, 'view': view, 'absent': False,
             'coordinate': artifact['coordinate'], 'artifact_id': artifact['artifact_id'],
             'body_sha256': artifact['body_sha256'], 'commitments_sha256': artifact['commitments_sha256'],
             'public_text_sha256': artifact['public_text_sha256'],
             'delivery_status': artifact['delivery_status'], 'envelope_status': artifact['envelope_status'],
             'aliases_previous': artifact['coordinate'] == previous_coord}
    lines = [f'Source {source}: {label(artifact["coordinate"])}; selected view: {view}',
             'Artifact: ' + artifact['artifact_id'], 'Original body SHA256: ' + artifact['body_sha256'],
             'Original commitments SHA256: ' + artifact['commitments_sha256'],
             'Delivery: ' + artifact['delivery_status'] + '; envelope: ' + artifact['envelope_status']]
    if view in ('body', 'both'):
        lines.extend(['BODY', artifact['body']])
    if view in ('commitments', 'both'):
        lines.extend(['COMMITMENTS', artifact['commitments']])
    return '\n'.join(lines), trace

def render_node(repo, output, coord, context=None):
    material, plan = context if context is not None else verify(repo, output)
    problem = problem_for(material, coord['problem'])
    nodes = nodes_for(material, problem, coord['arm'], coord['cycle'])
    node = next((n for n in nodes if n['id'] == coord['node']), None)
    if node is None:
        raise ValueError('UNKNOWN_NODE')
    paired_tid = problem['templates'][coord['cycle'] - 1]
    tid = coord['arm'] + '1' if coord['arm'] in BASELINE_ARMS else paired_tid
    bindings = node['inputs']
    if coord['arm'] in BASELINE_ARMS:
        bindings = [{'source': 'previous', 'view': 'both'}]
        if coord['cycle'] > 2:
            bindings.append({'source': 'origin', 'view': 'both'})
    previous_coord = source_coordinate(material, problem, coord, 'previous')
    projections, visible, originals, dependencies, barriers = [], [], {}, {}, {}
    for binding in bindings:
        source = source_coordinate(material, problem, coord, binding['source'])
        artifact = read_artifact(output, source) if source else None
        text, trace = project(binding['source'], binding['view'], artifact, previous_coord)
        projections.append(text)
        visible.append(trace)
        if source:
            originals[label(source)] = artifact
            dependencies[label(source)] = source
    if coord['node'] == nodes[-1]['id']:
        for earlier in nodes[:-1]:
            prior = coordinate(coord['problem'], coord['arm'], coord['cycle'], earlier['id'])
            barriers[label(prior)] = prior
    if coord['cycle'] > 1:
        for earlier in nodes_for(material, problem, coord['arm'], coord['cycle'] - 1):
            prior = coordinate(coord['problem'], coord['arm'], coord['cycle'] - 1, earlier['id'])
            barriers[label(prior)] = prior
    for key, prior in barriers.items():
        read_artifact(output, prior)
        dependencies[key] = prior
    projection_records = []
    if coord['arm'].startswith('mini_'):
        compiled = compile_manifest(Path(output) / 'manifests' / (tid + '.json'))
        state, blobs = MiniState(), MemoryBlobs()
        seq, previous_event = 0, compiled.genesis
        def add(stage, body, commitments, *, original=None, cycle=None):
            nonlocal seq, previous_event
            if stage.kind_id in compiled.kinds:
                submission = read_submission(json.dumps({'body': body, 'commitments': commitments},
                                                        ensure_ascii=False), compiled.kinds[stage.kind_id], 'both')
            else:
                submission = Submission(body, commitments, (), (), (), {})
            aid, br, cr = _store_artifact(blobs, stage, submission, seq)
            if original:
                if (br != original['body_ref'] or cr != original['commitments_ref']):
                    raise ValueError('ORIGINAL_ARTIFACT_REFS_CHANGED')
                aid = original['artifact_id']
            event = build_event(seq=seq, prev=previous_event, type=ARTIFACT_SUBMITTED,
                                cycle=coord['cycle'] if cycle is None else cycle,
                                stage_id=stage.stage_id, kind_id=stage.kind_id, artifact_id=aid,
                                body_ref=br, commitments_ref=cr,
                                payload={'seat': stage.seat, 'completion_tokens': 0})
            apply_event(state, event)
            seq, previous_event = seq + 1, event.event_id
            if blobs.get(br) != body.encode('utf-8') or blobs.get(cr) != commitments.encode('utf-8'):
                raise ValueError('RECONSTRUCTED_ARTIFACT_CHANGED')
            return {'artifact_id': aid, 'body_ref': br, 'commitments_ref': cr}
        for original in originals.values():
            source = original['coordinate']
            add(Stage(label(source), 'h005.authored.v1', (), False), original['body'],
                original['commitments'], original=original, cycle=source['cycle'])
        task_record = add(compiled.stage('task'), problem['prose'], '')
        for index, projected in enumerate(projections):
            row = add(compiled.stage(projection_id(node['id'], index)), projected, '')
            row.update({'selected_source': visible[index], 'machine_projection': True})
            projection_records.append(row)
        brief, exposed = render_brief(compiled, state, blobs, compiled.stage(node['id']), coord['cycle'])
        if exposed or not brief.endswith(ENVELOPE):
            raise ValueError('UNEXPECTED_CANONICAL_RENDER_CONTRACT')
        rendering = 'canonical_compile_reducer_render'
    else:
        parts = ['## Node ' + node['id'], node['instruction'], '## Original problem', problem['prose']]
        for index, projected in enumerate(projections):
            parts.extend(['## Selected input ' + bindings[index]['source'], projected])
        parts.append(ENVELOPE)
        brief, rendering, task_record = '\n\n'.join(parts), 'direct_explicit_views', None
    policy = material['formal_instruction'] if coord['arm'] == 'mini_fcl' else material['prose_instruction']
    messages = [{'role': 'system', 'content': material['system'] + '\n\n' + policy + '\n\n' + PUBLIC_CONTRACT},
                {'role': 'user', 'content': brief}]
    trace = {'schema': 'minireason.h005.trace.v1', 'coordinate': coord, 'template_id': tid,
             'paired_template_id': paired_tid, 'rendering': rendering, 'visible_sources': visible,
             'projection_artifacts': projection_records, 'task_artifact': task_record,
             'barrier_dependencies': list(barriers.values()),
             'origin_aliases_previous': coord['cycle'] == 2,
             'original_brief': brief, 'original_brief_sha256': sha(brief.encode('utf-8')),
             'fixture': 'Reconstructed reducer counters are not provider usage.'}
    settings = settings_for(coord['arm'])
    request = {'schema': 'minireason.h005.request.v1', 'coordinate': coord, 'plan_id': plan['plan_id'],
               'template_id': tid, 'paired_template_id': paired_tid, 'messages': messages, 'messages_sha256': digest(messages),
               'provider_payload': payload_for(messages, settings), 'settings': settings.to_dict(),
               'trace_sha256': digest(trace), 'dependencies': list(dependencies.values())}
    return request, trace


def arm_stopped(output, material, problem, arm, through_cycle):
    failed = False
    for cycle in range(1, through_cycle + 1):
        for node in nodes_for(material, problem, arm, cycle):
            coord = coordinate(problem['id'], arm, cycle, node['id'])
            response = at(output, 'responses', coord)
            if at(output, 'attempts', coord).exists() and not response.exists():
                raise ValueError('UNRESOLVED_ATTEMPT')
            if response.exists() and read_terminal(output, coord)['status'] == 'FAILED':
                failed = True
    return failed


def ready_coordinates(output, material, problem, cycle):
    queues = []
    for arm in ARMS:
        nodes = nodes_for(material, problem, arm, cycle)
        if arm_stopped(output, material, problem, arm, cycle):
            queues.append([])
            continue
        if cycle > 1:
            previous = [coordinate(problem['id'], arm, cycle - 1, node['id'])
                        for node in nodes_for(material, problem, arm, cycle - 1)]
            if not all(at(output, 'responses', coord).exists() for coord in previous):
                raise ValueError('PREVIOUS_TEMPLATE_NOT_COMPLETE')
        ready = []
        for index, node in enumerate(nodes):
            coord = coordinate(problem['id'], arm, cycle, node['id'])
            if at(output, 'responses', coord).exists():
                continue
            parents = [source_coordinate(material, problem, coord, b['source']) for b in node['inputs']]
            if index == len(nodes) - 1:
                parents += [coordinate(problem['id'], arm, cycle, n['id']) for n in nodes[:index]]
            if all(parent is None or at(output, 'responses', parent).exists() for parent in parents):
                ready.append(coord)
        queues.append(ready)
    selected = []
    while len(selected) < 5 and any(queues):
        for queue in queues:
            if queue and len(selected) < 5:
                selected.append(queue.pop(0))
    return selected


def wave_path(output, wave_id):
    if not re.fullmatch(r'wave[0-9]{4}', wave_id):
        raise ValueError('INVALID_WAVE_ID')
    return Path(output) / 'waves' / (wave_id + '.json')


def prepare_wave(repo, output, problem_id, cycle):
    material, plan = verify(repo, output)
    problem = problem_for(material, problem_id)
    selected = ready_coordinates(output, material, problem, cycle)
    existing = sorted((Path(output) / 'waves').glob('wave*.json'))
    for path in existing:
        if any(not at(output, 'responses', coord).exists() for coord in load(path)['coordinates']):
            raise ValueError('PREPARED_WAVE_PENDING')
    if not selected:
        return {'wave_id': None, 'coordinates': []}
    pending = []
    for coord in selected:
        if any(at(output, category, coord).exists()
               for category in ('requests', 'traces', 'attempts', 'responses', 'artifacts')):
            raise FileExistsError('COORDINATE_EXISTS')
        request, trace = render_node(repo, output, coord, (material, plan))
        pending.append((coord, request, trace))
    wave_id = f'wave{len(existing) + 1:04d}'
    wave = {'schema': 'minireason.h005.wave.v1', 'wave_id': wave_id, 'plan_id': plan['plan_id'],
            'problem': problem_id, 'cycle': cycle, 'coordinates': selected,
            'request_hashes': {label(coord): digest(request) for coord, request, _ in pending}}
    for coord, request, trace in pending:
        write_new(at(output, 'requests', coord), request)
        write_new(at(output, 'traces', coord), trace)
    write_new(wave_path(output, wave_id), wave)
    return wave

def required_paths(repo, output, wave):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    material, plan = verify(repo, output)
    paths = {output / 'plan.json', output / 'material.json', Path(__file__).resolve(),
             wave_path(output, wave['wave_id'])}
    paths.update(safe_source(repo, p) for p in {**plan['runtime_pins'], **plan['source_pins']})
    paths.update(output / 'manifests' / (tid + '.json') for tid in material['templates'])
    visited = set()
    def add(coord, terminal):
        identity = (label(coord), terminal)
        if identity in visited:
            return
        visited.add(identity)
        paths.update(at(output, category, coord) for category in ('requests', 'traces'))
        request = load(at(output, 'requests', coord))
        if terminal:
            read_artifact(output, coord)
            paths.update(at(output, category, coord) for category in ('attempts', 'responses', 'artifacts'))
            paths.add(at(output, 'responses', coord, 'txt'))
            paths.update(provider_dir(output, coord) / name
                         for name in ('call-0001.request.json', 'call-0001.response.json'))
        for parent in request['dependencies']:
            add(parent, True)
    for coord in wave['coordinates']:
        add(coord, False)
    return sorted(paths)


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE, timeout=90)


def check_published(repo, output, wave):
    repo = Path(repo).resolve()
    head = git(repo, 'rev-parse', 'HEAD').decode('ascii').strip()
    remote = git(repo, 'ls-remote', '--refs', 'origin', 'refs/heads/main').decode('ascii').split()
    if not remote or remote[0] != head:
        raise ValueError('REMOTE_MAIN_CHANGED')
    for path in required_paths(repo, output, wave):
        name = path.resolve().relative_to(repo).as_posix()
        if git(repo, 'show', head + ':' + name) != path.read_bytes():
            raise ValueError('INPUT_NOT_PUBLISHED')
    return head


def send_wave(repo, output, wave_id, *, provider_factory=None, publication_check=None, notify=print):
    material, plan = verify(repo, output)
    wave = load(wave_path(output, wave_id))
    if wave['wave_id'] != wave_id or wave['plan_id'] != plan['plan_id']:
        raise ValueError('WAVE_PLAN_CHANGED')
    selected = wave['coordinates']
    if not 1 <= len(selected) <= 5:
        raise ValueError('WAVE_SIZE_INVALID')
    for coord in selected:
        if at(output, 'attempts', coord).exists() or at(output, 'responses', coord).exists():
            raise FileExistsError('NO_REPLAY')
    problem = problem_for(material, wave['problem'])
    if selected != ready_coordinates(output, material, problem, wave['cycle']):
        raise ValueError('WAVE_NOT_DEPENDENCY_READY')
    requests = {}
    for coord in selected:
        request, trace = render_node(repo, output, coord, (material, plan))
        if (load(at(output, 'requests', coord)) != request or load(at(output, 'traces', coord)) != trace
                or wave['request_hashes'][label(coord)] != digest(request)):
            raise ValueError('REQUEST_OR_TRACE_CHANGED')
        requests[label(coord)] = request
    head = (publication_check or check_published)(repo, output, wave)
    if provider_factory is None and not os.environ.get('DEEPSEEK_API_KEY'):
        raise ValueError('KEY_MISSING')
    factory = provider_factory or DeepSeek
    def send(coord):
        request = requests[label(coord)]
        settings = settings_for(coord['arm'])
        write_new(at(output, 'attempts', coord),
                  {'schema': 'minireason.h005.attempt.v1', 'coordinate': coord,
                   'request_sha256': digest(request), 'published_commit': head,
                   'wave_id': wave_id, 'started_utc': utc(), 'automatic_retry': False})
        failure_type = None
        try:
            provider = factory(settings, provider_dir(output, coord))
            provider.complete(request['messages'], json_output=True,
                              coordinate={'harness': 'H005', **coord})
        except Exception as exc:
            failure_type = type(exc).__name__
        response_path = provider_dir(output, coord) / 'call-0001.response.json'
        provider_request_path = provider_dir(output, coord) / 'call-0001.request.json'
        receipt = {'schema': 'minireason.h005.receipt.v1', 'coordinate': coord,
                   'request_sha256': digest(request), 'finished_utc': utc(), 'status': 'FAILED',
                   'failure_type': failure_type, 'envelope_status': None, 'usage': None,
                   'returned_model': None, 'finish_reason': None,
                   'provider_request_sha256': sha(provider_request_path.read_bytes()) if provider_request_path.exists() else None,
                   'provider_response_sha256': sha(response_path.read_bytes()) if response_path.exists() else None}
        try:
            record = load(response_path)
            receipt.update({'usage': record.get('usage'), 'returned_model': record.get('returned_model'),
                            'finish_reason': record.get('finish_reason')})
            if isinstance(record.get('content'), str):
                write_new(at(output, 'responses', coord, 'txt'), record['content'].encode('utf-8'))
            contribution = decode_contribution(record, request['provider_payload'], settings)
            provider_request = load(provider_request_path)
            if (provider_request.get('request') != request['provider_payload']
                    or provider_request.get('request_sha256') != digest(request['provider_payload'])
                    or provider_request.get('settings') != settings.to_dict()
                    or provider_request.get('coordinate') != {'harness': 'H005', **coord}
                    or record.get('coordinate') != {'harness': 'H005', **coord}):
                raise ValueError('PROVIDER_REQUEST_FILE_CHANGED')
            artifact = authored_artifact(coord, contribution)
            write_new(at(output, 'artifacts', coord), artifact)
            receipt.update({'status': contribution['delivery_status'],
                            'envelope_status': contribution['envelope_status'],
                            'artifact_sha256': sha(at(output, 'artifacts', coord).read_bytes())})
        except Exception as exc:
            receipt['validation_failure_type'] = type(exc).__name__
        write_new(at(output, 'responses', coord), receipt)
        notify(json.dumps({'coordinate': coord, 'status': receipt['status'],
                           'envelope_status': receipt['envelope_status'], 'usage': receipt['usage']}))
        return receipt
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for future in as_completed([executor.submit(send, coord) for coord in selected]):
            results.append(future.result())
    return sorted(results, key=lambda r: label(r['coordinate']))


def audit(repo, output):
    material, plan = verify(repo, output)
    counts = {'COMPLETE': 0, 'PARTIAL': 0, 'FAILED': 0, 'OPAQUE': 0,
              'unresolved_attempts': 0, 'unvisited': 0}
    usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    unknown_usage, invocations = 0, []
    for problem in material['problems']:
        for arm in ARMS:
            for cycle in range(1, len(problem['templates']) + 1):
                statuses = []
                for node in nodes_for(material, problem, arm, cycle):
                    coord = coordinate(problem['id'], arm, cycle, node['id'])
                    if at(output, 'responses', coord).exists():
                        receipt = read_terminal(output, coord)
                        status = receipt['status']
                        counts[status] += 1
                        if receipt['envelope_status'] == 'OPAQUE':
                            counts['OPAQUE'] += 1
                        tokens = receipt['usage']
                        if isinstance(tokens, dict) and all(type(tokens.get(k)) is int for k in usage):
                            for name in usage:
                                usage[name] += tokens[name]
                        else:
                            unknown_usage += 1
                    elif at(output, 'attempts', coord).exists():
                        status = 'UNRESOLVED'
                        counts['unresolved_attempts'] += 1
                        unknown_usage += 1
                    else:
                        status = 'UNVISITED'
                        counts['unvisited'] += 1
                    statuses.append(status)
                invocations.append({'problem': problem['id'], 'arm': arm, 'cycle': cycle,
                                    'template_id': arm + '1' if arm in BASELINE_ARMS else problem['templates'][cycle - 1],
                                    'paired_template_id': problem['templates'][cycle - 1], 'nodes': len(statuses),
                                    'complete': all(s in ('COMPLETE', 'PARTIAL') for s in statuses)})
    return {'plan_id': plan['plan_id'], 'max_calls': plan['max_calls'], 'counts': counts,
            'known_usage': usage, 'unknown_usage_calls': unknown_usage, 'invocations': invocations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('initialize', 'verify', 'prepare-wave', 'send-wave', 'audit'))
    parser.add_argument('--repo', type=Path, default=REPOSITORY)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--material', type=Path)
    parser.add_argument('--problem')
    parser.add_argument('--cycle', type=int)
    parser.add_argument('--wave')
    args = parser.parse_args()
    prompted = False
    try:
        if args.operation == 'initialize':
            if args.material is None:
                raise ValueError('MATERIAL_ARGUMENT_REQUIRED')
            plan = initialize(args.repo, args.output, args.material)
            result = {'plan_id': plan['plan_id'], 'max_calls': plan['max_calls']}
        elif args.operation == 'verify':
            _, plan = verify(args.repo, args.output)
            result = {'plan_id': plan['plan_id'], 'verified': True}
        elif args.operation == 'prepare-wave':
            result = prepare_wave(args.repo, args.output, args.problem, args.cycle)
        elif args.operation == 'send-wave':
            if os.environ.get('DEEPSEEK_KEY_INPUT') == 'prompt':
                if not sys.stdin.isatty():
                    raise ValueError('KEY_PROMPT_REQUIRES_TTY')
                os.environ['DEEPSEEK_API_KEY'] = getpass.getpass('DeepSeek API key: ')
                prompted = True
            receipts = send_wave(args.repo, args.output, args.wave)
            result = {'wave_id': args.wave, 'terminal': len(receipts),
                      'statuses': [r['status'] for r in receipts]}
        else:
            result = audit(args.repo, args.output)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        code = str(exc)
        print(json.dumps({'error': code if re.fullmatch('[A-Z0-9_]+', code) else type(exc).__name__}))
        return 2
    finally:
        if prompted:
            os.environ.pop('DEEPSEEK_API_KEY', None)


if __name__ == '__main__':
    raise SystemExit(main())
