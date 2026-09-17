#!/usr/bin/env python3
"""R003 draft matrix launcher; offline by default, live deliberately unavailable.

This delegates to tools/reason.py without modifying the published instruments.
Target R003 conditions currently refuse under their exact R002 pins. `smoke`
exercises the existing prose CLI and is NOT a target-condition observation.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[2]
WORK = ROOT / 'work/review25'
PYTHON = Path('C:/Users/darre/AppData/Local/Programs/Python/Python311/python.exe')
CONDITIONS = ('NATIVE', 'LOOP-CROSS', 'LOOP-DECOMPOSED')
ALIASES = dict(zip(CONDITIONS, ('n', 'x', 'd')))
RECIPES = {'LOOP-CROSS': 'r003-cross-a2-draft.json',
           'LOOP-DECOMPOSED': 'r003-decomposed-closing-draft.json'}
LIVE_HOLD = 'DRAFT_LIVE_HOLD: independent sealed briefs and installed R003 instrument support are pending'

class Refused(RuntimeError):
    pass

def utc():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(path):
    with Path(path).open(encoding='utf-8', newline='') as f:
        return json.load(f)

def allowed(path):
    path = Path(path).resolve()
    if not (path.is_relative_to(WORK.resolve()) or path.is_relative_to(STUDY)):
        raise Refused('WRITE_OUTSIDE_AUTHORIZED_SCOPE')
    return path

def put(path, obj):
    path = allowed(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
        f.flush()
        os.fsync(f.fileno())

def activity(phase, action, paths, outcome=None):
    import uuid
    sys.path.insert(0, str(ROOT / 'tools'))
    from repo_activity import append
    append(dict(timestamp_utc=utc(), event_id=uuid.uuid4().hex, agent='root-review25',
        decision='REC-20260917-B', phase=phase, action=action, paths=[str(p) for p in paths],
        why='Verify draft R003 custody offline', goal='Recorded trial-and-error design',
        outcome=outcome))

@contextmanager
def lock(directory):
    directory = allowed(directory)
    directory.mkdir(parents=True, exist_ok=True)
    marker = directory / '.r003-launcher-lock'
    try:
        with marker.open('x', encoding='utf-8', newline='') as f:
            f.write(utc())
    except FileExistsError:
        raise Refused('LAUNCHER_BUSY_OR_STALE_LOCK: inspect before removing a stale lock')
    try:
        yield
    finally:
        marker.unlink()

def hash_tree(path):
    return {p.relative_to(path).as_posix(): digest(p)
            for p in sorted(path.rglob('*')) if p.is_file()}

def sources():
    paths = [Path(__file__), ROOT / 'tools/reason.py']
    for directory in (ROOT / 'src/minireason', ROOT / 'experiments/diagnostics/R002-episodes-under-calibrated-difficulty/contracts',
                      ROOT / 'experiments/diagnostics/R002-episodes-under-calibrated-difficulty/recipes'):
        paths.extend(p for p in directory.rglob('*') if p.is_file() and p.suffix in {'.py', '.json'})
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(set(paths))}

def copy_text(source, target):
    with Path(source).open(encoding='utf-8', newline='') as f:
        text = f.read()
    target = allowed(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8', newline='') as f:
        f.write(text)
    if digest(source) != digest(target):
        raise Refused('COPY_HASH_MISMATCH')

def argv_for(directory, problem, condition, mode):
    cmd = [str(PYTHON), '-B', '-X', 'utf8', str(ROOT / 'tools/reason.py'),
           'run-r002-native' if condition == 'NATIVE' else 'run-r002',
           '--problem', str(directory / 'p' / (problem + '.txt')),
           '--out', str(directory / 'r' / problem / ALIASES[condition]),
           '--mode', mode, '--relations', str(directory / 'inputs/RELATIONS.json'),
           '--attempt-policy', 'strict', '--prompt-token-cap', '32768',
           '--retry-transport', '0', '--env-file', '.env']
    if condition == 'NATIVE':
        cmd += ['--condition', 'NATIVE', '--thinking', 'native', '--reasoning-effort', 'medium',
                '--completion-tokens', '32768']
    else:
        cmd += ['--cycles', '3', '--recipe', str(directory / 'inputs' / RECIPES[condition]),
                '--fork-registry', str(directory / 'inputs/FORKS.json'),
                '--coding-manifest', str(directory / 'inputs/CODINGS.json')]
    # Live token-bound and capability arguments cannot be fabricated. The hard hold
    # precedes dispatch; COMMANDS.md names the additional qualified files needed.
    return cmd

def create(series, problems, conditions, question, mode, parent=None, reason=None, cells=None):
    if mode == 'live':
        raise Refused(LIVE_HOLD)
    if not question.strip() or '\n' in question or '\r' in question:
        raise Refused('ONE_LINE_OCCURRENCE_QUESTION_REQUIRED')
    if len(set(problems)) != len(problems) or len(set(conditions)) != len(conditions):
        raise Refused('DUPLICATE_MATRIX_ENTRY')
    for problem in problems:
        if not re.fullmatch(r'O0[1-8]', problem):
            raise Refused('INVALID_PROBLEM_ID')
        p = STUDY / 'problems' / (problem + '.txt')
        if not p.is_file() or not p.read_text(encoding='utf-8').strip():
            raise Refused('PROBLEM_MISSING_OR_EMPTY: ' + problem)
    if not conditions or any(c not in CONDITIONS for c in conditions):
        raise Refused('UNSUPPORTED_CONDITION')
    series = allowed(series)
    with lock(series):
        numbers = [int(p.name[1:]) for p in series.iterdir() if p.is_dir() and re.fullmatch(r'o\d{3,}', p.name)]
        directory = series / ('o%03d' % (max(numbers, default=0) + 1))
        directory.mkdir()
        put(directory / 'QUESTION.json', dict(utc=utc(), question=question,
            state='declared_before_dispatch', parent=str(parent) if parent else None, reason=reason))
        for problem in problems:
            copy_text(STUDY / 'problems' / (problem + '.txt'), directory / 'p' / (problem + '.txt'))
        for name in ('RELATIONS.json', 'FORKS.json', 'CODINGS.json'):
            copy_text(STUDY / 'public' / name, directory / 'inputs' / name)
        for condition in conditions:
            if condition in RECIPES:
                name = RECIPES[condition]
                copy_text(STUDY / 'recipes' / name, directory / 'inputs' / name)
        selected = cells or [(p, c) for p in problems for c in conditions]
        rows = [dict(problem=p, condition=c, alias=ALIASES[c],
                     output='r/' + p + '/' + ALIASES[c],
                     argv=argv_for(directory, p, c, mode if mode != 'plan' else 'live')) for p, c in selected]
        manifest = dict(schema='minireason.r003.matrix.v1', occurrence=directory.name,
            created_utc=utc(), mode=mode, question=question, matrix=rows,
            order='problem then condition, listed order, deterministic; no random seed used',
            brief_status='PENDING_UNWRITTEN', live_hold=LIVE_HOLD,
            source_sha256=sources(), input_sha256={**{'p/'+k:v for k,v in hash_tree(directory/'p').items()},
                                                  **{'inputs/'+k:v for k,v in hash_tree(directory/'inputs').items()}},
            parent=str(parent) if parent else None, reason=reason)
        put(directory / 'MANIFEST.json', manifest)
    return directory

def verify(directory):
    directory = allowed(directory)
    manifest = read_json(directory / 'MANIFEST.json')
    if manifest['schema'] != 'minireason.r003.matrix.v1':
        raise Refused('MANIFEST_SCHEMA')
    for path, expected in manifest['source_sha256'].items():
        if digest(ROOT / path) != expected:
            raise Refused('SOURCE_CHANGED: ' + path)
    for path, expected in manifest['input_sha256'].items():
        target = (directory / path).resolve()
        if not target.is_relative_to(directory) or digest(target) != expected:
            raise Refused('INPUT_CHANGED')
    for row in manifest['matrix']:
        mode = manifest['mode'] if manifest['mode'] != 'plan' else 'live'
        if row['argv'] != argv_for(directory, row['problem'], row['condition'], mode):
            raise Refused('COMMAND_CHANGED')
        expected_output = 'r/' + row['problem'] + '/' + ALIASES[row['condition']]
        if row['output'] != expected_output:
            raise Refused('OUTPUT_CHANGED')
        result_path = directory / 'results' / (row['problem'] + '-' + row['alias'] + '.json')
        if result_path.exists():
            saved = read_json(result_path)
            actual = hash_tree(directory / row['output']) if (directory / row['output']).exists() else {}
            if saved['evidence_sha256'] != actual:
                raise Refused('SAVED_EVIDENCE_CHANGED')
    return manifest

def execute(directory):
    manifest = verify(directory)
    if manifest['mode'] == 'live':
        raise Refused(LIVE_HOLD)
    if manifest['mode'] == 'plan':
        return {'status': 'STAGED_NOT_RUN', 'rows': len(manifest['matrix'])}
    env = {name: os.environ[name] for name in os.environ
           if not name.endswith('_API_KEY') and name not in {'API_KEY', 'OPENAI_ACCESS_TOKEN'}}
    # Remove credentials by NAME only, without reading or printing their values.
    for name in tuple(env):
        if name.endswith('_API_KEY') or name in {'API_KEY', 'OPENAI_ACCESS_TOKEN'}:
            env.pop(name, None)
    env.update(PYTHONPATH='src;tests', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
               PYTHONDONTWRITEBYTECODE='1', TMP='C:/tr25', GIT_OPTIONAL_LOCKS='0')
    with lock(directory):
        for row in manifest['matrix']:
            key = row['problem'] + '-' + row['alias']
            result_path = directory / 'results' / (key + '.json')
            intent_path = directory / 'intents' / (key + '.json')
            if result_path.exists():
                continue
            if intent_path.exists() or (directory / row['output']).exists():
                raise Refused('INDETERMINATE_ATTEMPT: inspect original custody; never resend')
            put(intent_path, dict(utc=utc(), argv=row['argv'], mode='offline', question=manifest['question']))
            activity('begin', 'Dispatch actual offline reason.py target command', [row['output']])
            try:
                completed = subprocess.run(row['argv'], cwd=ROOT, env=env, capture_output=True,
                                           text=True, encoding='utf-8', timeout=60)
            except (OSError, subprocess.TimeoutExpired):
                activity('outcome', 'Offline dispatch incomplete', [row['output']], 'intent retained; do not resend')
                raise Refused('OFFLINE_DISPATCH_INDETERMINATE') from None
            output = directory / row['output']
            state = read_json(output / 'state.json') if (output / 'state.json').exists() else {}
            status = 'OFFLINE_COMPLETE' if completed.returncode == 0 else 'OFFLINE_REFUSED_OR_FAILED'
            result = dict(utc=utc(), status=status, returncode=completed.returncode,
                          stdout=completed.stdout, stderr=completed.stderr,
                          stop_reason=state.get('stop_reason'), evidence_sha256=hash_tree(output) if output.exists() else {},
                          claim='Offline plumbing only; no participant/model evidence', provider_calls=0)
            put(result_path, result)
            activity('outcome', 'Dispatch actual offline reason.py target command', [row['output']], status)
            print(key + ': ' + status + ' rc=' + str(completed.returncode))
    return {'status': 'OFFLINE_FINISHED', 'rows': len(manifest['matrix']), 'failed': sum(read_json(directory / 'results' / (r['problem'] + '-' + r['alias'] + '.json'))['returncode'] != 0 for r in manifest['matrix'])}

def rerun(directory, question, reason, mode):
    if not reason or not reason.strip():
        raise Refused('RERUN_REASON_REQUIRED')
    prior = verify(directory)
    failed = []
    for row in prior['matrix']:
        p = directory / 'results' / (row['problem'] + '-' + row['alias'] + '.json')
        if not p.exists():
            raise Refused('UNRESOLVED_OR_UNSTARTED_CELL: inspect before selecting a rerun')
        if read_json(p)['returncode'] != 0:
            failed.append((row['problem'], row['condition']))
    if not failed:
        raise Refused('NO_KNOWN_FAILED_CELLS')
    # Source changes require a fresh declared occurrence, not this same-source retry helper.
    result = create(directory.parent, list(dict.fromkeys(p for p,c in failed)),
                    list(dict.fromkeys(c for p,c in failed)), question, mode,
                    parent=directory, reason=reason, cells=failed)
    return result

def smoke(out):
    out = allowed(out)
    if out.exists():
        raise Refused('SMOKE_OUTPUT_EXISTS')
    # Actual legacy published route. Explicitly no --env-file: legacy `run` loads
    # an env-file even offline. R002 subcommands defer it and are safe above.
    cmd = [str(PYTHON), '-B', '-X', 'utf8', str(ROOT/'tools/reason.py'), 'run',
           '--problem', str(STUDY/'problems/O01.txt'), '--cycles', '3',
           '--recipe', 'cross-family', '--mode', 'offline', '--out', str(out)]
    env = {name: os.environ[name] for name in os.environ
           if not name.endswith('_API_KEY') and name not in {'API_KEY', 'OPENAI_ACCESS_TOKEN'}}
    for name in tuple(env):
        if name.endswith('_API_KEY') or name == 'API_KEY': env.pop(name, None)
    env.update(PYTHONPATH='src;tests', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
               PYTHONDONTWRITEBYTECODE='1', TMP='C:/tr25', GIT_OPTIONAL_LOCKS='0')
    activity('begin', 'Published prose CLI O01 offline smoke; not an R003 condition', [out])
    result = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=60)
    put(out.parent/(out.name+'-receipt.json'), dict(utc=utc(), argv=cmd, returncode=result.returncode,
        stdout=result.stdout, stderr=result.stderr, evidence_sha256=hash_tree(out) if out.exists() else {},
        provider_calls=0, claim='Legacy fixture, not R003 NATIVE/CROSS/DECOMPOSED qualification'))
    activity('outcome', 'Published prose CLI O01 offline smoke; not an R003 condition', [out], result.returncode)
    print(result.stdout, end='')
    print(result.stderr, end='', file=sys.stderr)
    return result.returncode

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('new')
    p.add_argument('--series', type=Path, default=WORK/'series')
    p.add_argument('--problems', nargs='+', default=['O%02d'%i for i in range(1,9)])
    p.add_argument('--conditions', nargs='+', choices=CONDITIONS, default=list(CONDITIONS))
    p.add_argument('--question', required=True)
    p.add_argument('--mode', choices=['plan','offline','live'], default='plan')
    for name in ('resume','status','rerun-failed'):
        p = sub.add_parser(name);p.add_argument('--occurrence', type=Path, required=True)
        if name == 'rerun-failed':
            p.add_argument('--question', required=True);p.add_argument('--reason', required=True)
            p.add_argument('--mode', choices=['plan','offline','live'], default='plan')
    p = sub.add_parser('smoke');p.add_argument('--out', type=Path, default=WORK/'smoke')
    args = parser.parse_args(argv)
    activity('begin', 'R003 launcher '+args.command, [STUDY, WORK])
    try:
        if args.command == 'smoke': return smoke(args.out)
        if args.command == 'new':
            directory = create(args.series, args.problems, args.conditions, args.question, args.mode)
        else:
            directory = allowed(args.occurrence)
        if args.command == 'rerun-failed':
            directory = rerun(directory, args.question, args.reason, args.mode)
        result = verify(directory) if args.command == 'status' else execute(directory)
        print(json.dumps({'occurrence':str(directory), 'result':result}, ensure_ascii=False))
        activity('outcome', 'R003 launcher '+args.command, [directory], 'finished')
        return 2 if result.get('failed', 0) else 0
    except (Refused, OSError, ValueError, KeyError) as error:
        detail = str(error) if isinstance(error, Refused) else type(error).__name__
        activity('outcome', 'R003 launcher '+args.command, [WORK], 'refused: '+detail)
        print('R003_REFUSED: '+detail, file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
