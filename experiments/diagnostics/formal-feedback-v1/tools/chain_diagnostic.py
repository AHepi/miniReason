#!/usr/bin/env python3
"""Operator-authored dependency probes; no LLM or general proof assistant."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

from formal_argument_check import check_argument, load_json


def check_chain(base, steps):
    """Check each declared step before permitting its reuse by descendants.

    Every step receives all base assumptions plus its named earlier steps.
    A dependency is usable only when this exact checker found it entailed
    under nonempty premise models. Metadata/meaning adequacy is not checked.
    """
    known = {entry['id'] for entry in base['premises']}
    for step in steps:
        if set(step) != {'id', 'formula', 'depends_on'}:
            raise ValueError('Step must contain id, formula and depends_on')
        if step['id'] in known:
            raise ValueError('Duplicate or shadowed step identifier')
        if len(set(step['depends_on'])) != len(step['depends_on']):
            raise ValueError('Duplicate dependency')
        if any(dep not in known for dep in step['depends_on']):
            raise ValueError('Unknown, self or forward dependency')
        known.add(step['id'])
    base_ids = {entry['id'] for entry in base['premises']}
    accepted, receipts = {}, []
    for step in steps:
        blockers = [dep for dep in step['depends_on']
                    if dep not in base_ids and dep not in accepted]
        if blockers:
            receipts.append({'step': copy.deepcopy(step), 'status': 'blocked',
                             'unestablished_dependencies': blockers})
            continue
        argument = copy.deepcopy(base)
        argument['goal'] = {'id': step['id'], 'formula': step['formula']}
        argument['premises'].extend(copy.deepcopy(accepted[dep])
                                   for dep in step['depends_on'] if dep in accepted)
        result = check_argument(argument)
        receipts.append({'step': copy.deepcopy(step), 'status': result['classification'],
                         'obligation': result})
        if result['classification'] == 'entailed':
            accepted[step['id']] = {'id': step['id'], 'formula': step['formula']}
    return {'original_base': copy.deepcopy(base), 'steps': receipts,
            'accepted_for_formal_reuse': list(accepted),
            'scope': 'Fixed finite interpretation only; no semantic endorsement, generated repair, or model observation.'}


def run_probes(fixture_dir):
    base = load_json(fixture_dir / 'conditional_entailment.json')
    base['premises'].append({'id': 'observed_ack', 'formula': 'ack'})
    steps = [
        {'id': 'step_a', 'formula': 'a', 'depends_on': ['ack_policy', 'observed_ack']},
        {'id': 'step_b', 'formula': 'b', 'depends_on': ['step_a']},
        {'id': 'step_safe', 'formula': 'safe', 'depends_on': ['step_a', 'step_b']},
    ]
    valid = check_chain(base, steps)
    weakened = copy.deepcopy(base)
    weakened['premises'][0]['formula'] = {'implies': ['ack', 'a']}
    blocked = check_chain(weakened, steps)
    naive = copy.deepcopy(weakened)
    naive['premises'].append({'id': 'assumed_unproved_b', 'formula': 'b'})
    naive['goal'] = {'id': 'naive_goal', 'formula': 'safe'}
    naive_result = check_argument(naive)
    contradictory = copy.deepcopy(base)
    contradictory['premises'].append({'id': 'denied_b', 'formula': {'not': 'b'}})
    inconsistent = check_chain(contradictory, steps)
    rejected = {}
    for label, altered in [
        ('self_dependency', [{'id': 'x', 'formula': 'a', 'depends_on': ['x']}]),
        ('forward_dependency', [{'id': 'x', 'formula': 'a', 'depends_on': ['y']},
                                {'id': 'y', 'formula': 'b', 'depends_on': []}]),
        ('shadowed_base_identifier', [{'id': 'ack_policy', 'formula': 'a', 'depends_on': []}]),
    ]:
        try:
            check_chain(base, altered)
        except ValueError as error:
            rejected[label] = str(error)
        else:
            raise RuntimeError('Dependency regression accepted: ' + label)
    expected = {
        'valid': [entry['status'] for entry in valid['steps']] == ['entailed'] * 3,
        'blocked': [entry['status'] for entry in blocked['steps']] == ['entailed', 'undetermined', 'blocked'],
        'inconsistent': [entry['status'] for entry in inconsistent['steps']] == ['inconsistent', 'blocked', 'blocked'],
        'naive_final_check': naive_result['classification'] == 'entailed',
        'three_dependency_errors_rejected': len(rejected) == 3,
    }
    if not all(expected.values()):
        raise RuntimeError('A predeclared diagnostic outcome failed: ' + str(expected))
    return {'provenance': 'Operator-authored illustrative probes, not LLM-generated reasoning.',
            'model_calls': 0, 'diagnostic_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'valid_chain': valid, 'unsupported_step_chain': blocked,
            'inconsistent_base_chain': inconsistent, 'naive_final_only_check': naive_result,
            'dependency_errors_rejected': rejected, 'expected_outcomes': expected,
            'interpretation': 'The naive check establishes a conditional result after adding b as an assumption. It does not validate the missing inference to b. The chain receipt exposes that distinction; neither route checks the prose mapping.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run_probes(args.fixtures)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'expected_outcomes': result['expected_outcomes'], 'model_calls': 0}))


if __name__ == '__main__':
    main()
