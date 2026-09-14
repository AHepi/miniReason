"""C001: three-case contrast triple at one responder node, plus a no-objection control.

One node (fork5 `response`), one instruction, one set of non-objection inputs; only the
`objection` projection block varies across four cases. Identities are deterministic: no
wall clock enters plan_id, any request digest or any artifact digest. No scoring, ranking
or merit field is produced anywhere.

Operations
  prepare  freeze plan.json (plan_id = digest of the plan body) and run the offline preflight
  run      dispatch by waves, write-once records, no replay, <=5 concurrent per key
           (--resume completes an interrupted occurrence without replaying a spent call)
  audit    re-tie every written coordinate to the frozen plan and re-derive its artifact
  table    render the mechanical comparison table and root's empty reading columns

Transport is `minireason.provider_openai_compat` (OpenAICompatProvider, OfflineProvider;
per-key semaphores of five shared process-wide). Endpoint/ENDPOINTS come from
`minireason/data/endpoints.json` beside the module actually imported -- the published
`src/minireason/` tree, or a staged provider package when MINIREASON_PROVIDER_SRC is set
and put ahead of it on PYTHONPATH. The module and the registry are pinned in
material.json.transport_pins and re-hashed by every operation (TRANSPORT_PIN_MISMATCH).

`max_tokens` AND `timeout_seconds` are declared per endpoint in the material, frozen in
the plan and recorded in every request. The registry file is never written: the declared
timeout is applied to the resolved `Endpoint` value by `dataclasses.replace` at provider
construction (`resolve_endpoint`), and any disagreement between the plan, the material,
the call spec, the written record and the transport's own settings view is refused as
TIMEOUT_NOT_APPLIED.

--- v2 ---------------------------------------------------------------------------
This file is the SUCCESSOR driver identity. It is a byte copy of
`tools/contrast_triple_study.py` at sha256
f5f9dfcadd8bdd769821213b5c09d569480daa20db3a5e8d8d763efd9e08688b, the bytes published
under REC-20260914-U and pinned as `helper_sha256` in C001 occurrence-01's `plan.json`.
v1 is NOT edited and cannot be: it writes its own sha256 into every plan it has already
built, folded into `plan_id`, so one changed byte would invalidate the published
occurrence-01 identity and every custody check that reads it.

Every difference from v1 is marked `# V2:` in the source, and this is the complete list:

  (a) this docstring;
  (b) `PARTIAL_UNRESOLVED`, a constant whose text named 8192 as the ceiling, becomes
      `partial_unresolved(ceiling)` over `PARTIAL_UNRESOLVED_TEMPLATE`, so a PARTIAL
      receipt names the ceiling the call actually ran under instead of a literal that
      is false whenever the endpoint's ceiling is not 8192;
  (c) its one call site in `decode_contribution`, which passes `spec['max_tokens']`;
  (d) `dispatch_scope`, an OPTIONAL material block naming the endpoint ids and arms an
      occurrence dispatches, validated in `validate_material`;
  (e) `scoped_endpoints`, `scoped_arms` and `planned_call_count`, three helpers that
      read it;
  (f) `all_coordinates`, which builds coordinates over the scope;
  (g) `plan_body`, whose `planned_calls` is the scoped count and which carries
      `dispatch_scope` into the frozen plan when one is declared;
  (h) `_offline_preflight`, which checks the built count against the plan's own
      `planned_calls` instead of against the module constant.

Nothing else moves. Where a material declares NO `dispatch_scope`, v2 is v1 in behaviour:
the scope helpers return the full endpoint and arm sets, `planned_call_count` returns
`PLANNED_CALLS`, no `dispatch_scope` key is written into the plan, and `plan_body` is
equal to v1's in every field except `helper_sha256` -- which differs by construction,
because it is this file's own digest, and which is precisely why the successor needs its
own identity rather than an amendment. `tests/test_contrast_triple_study_v2.py` proves
both claims: a diff proof that normalises this docstring away and refuses any hunk not
marked `# V2:`, and a v1-parity test that compares the two plan bodies field by field on
occurrence-01's own published material.

The scope narrows what is DISPATCHED. It does not narrow what is FROZEN: all eight briefs
(two arms x four cases) are still written and still hashed into the plan, the recoding,
carrier and control checks still run over both arms, and `RECODING_TABLE.md` still renders
all 85 units. An occurrence that dispatches one cell is still pre-registered against the
whole published correspondence table.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SCHEMA_MATERIAL = 'minireason.c001.material.v1'
CASES = ('original', 'recoding', 'carrier', 'control')
ARMS = ('fcl', 'prose')
REPLICATES = 5
MAX_TOKENS_DEFAULT = 8192        # the ceiling for an endpoint that sends no reasoning
MAX_TOKENS_AUTHORISED = 32768    # the highest ceiling any endpoint of this study may carry
# The wall-clock read timeout is declared PER ENDPOINT, exactly as max_tokens is, and is
# applied to the registry Endpoint by `dataclasses.replace` at provider construction.
# `endpoints.json` itself is never edited: it is a pinned published file, and a study
# that rewrote it would invalidate every other plan that pins the same bytes.
TIMEOUT_SECONDS_REGISTRY_DEFAULT = 180   # what the published registry declares for every row
TIMEOUT_SECONDS_AUTHORISED = 600         # the transport's own validation maximum (Endpoint)
AUTOMATIC_RETRIES = 0
MAX_CONCURRENT_PER_KEY = 5
ENDPOINT_COUNT = 6
PLANNED_CALLS = len(CASES) * REPLICATES * ENDPOINT_COUNT * len(ARMS)

SENTENCE = re.compile(r'(?<=[.!?])\s+')
BULLET = re.compile(r'^[ \t]*[-*\u2022]\s+')
SLUG_OK = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z')
REP_OK = re.compile(r'rep[1-9][0-9]?\Z')
FENCE = re.compile(r'\A\s*```[A-Za-z0-9_+-]*[ \t]*\r?\n(?P<inner>.*?)\r?\n?[ \t]*```\s*\Z', re.S)

# A label naming a comparison outcome is not a quantity. Nothing in this study may
# write a field whose name asserts one (FW5:851; PURPOSE.md, "no scalar progress meter").
FORBIDDEN_KEYS = frozenset({
    'score', 'scores', 'scoring', 'rank', 'ranking', 'ranks', 'merit', 'grade', 'grades',
    'rating', 'ratings', 'points', 'novelty', 'creativity', 'quality', 'winner', 'win',
    'best', 'worst', 'better', 'worse', 'weight', 'weights', 'percentile', 'verdict',
})

FCL_REF_FIELDS = ('target', 'depends', 'mentions', 'revises', 'withdraws')
FCL_TYPES = ('claim', 'commitment', 'objection', 'use', 'problem')

# Provider status / finish_reason pairs this study accepts as a delivery.
DELIVERY = {('COMPLETE', 'stop'): 'COMPLETE',
            ('USAGE_UNAVAILABLE', 'stop'): 'COMPLETE',
            ('INCOMPLETE_GENERATION', 'length'): 'PARTIAL'}

# V2: v1's constant named 8192 in its text, which is false of any endpoint whose declared
# ceiling is not 8192 -- and a receipt that misnames the ceiling it stopped at is a record
# of a configuration that did not happen. The text is now a template filled with the
# coordinate's own declared ceiling, taken from the call spec.
PARTIAL_UNRESOLVED_TEMPLATE = ('PARTIAL delivery: generation stopped at the {ceiling}-token '
                               'ceiling, so the commitment surface is truncated. The cell is '
                               'unresolved and is not compared against another case (FW5:634).')


def partial_unresolved(ceiling: int) -> str:
    """V2: the PARTIAL reason for a coordinate, naming its own declared ceiling."""
    if type(ceiling) is not int or not 1 <= ceiling <= MAX_TOKENS_AUTHORISED:
        raise ValueError('MATERIAL_ENDPOINT_MAX_TOKENS')
    return PARTIAL_UNRESOLVED_TEMPLATE.format(ceiling=ceiling)


# ------------------------------------------------------------------ primitives

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def tsha(text: str) -> str:
    return sha(text.encode('utf-8'))


def digest(value: Any) -> str:
    """Identity digest; identical to provider_openai_compat.digest. No wall clock, ever."""
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':')).encode('utf-8'))


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def load(path: Path) -> Any:
    return json.loads(Path(path).read_bytes())


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


ALWAYS_SCANNED_ENVS = ('DEEPSEEK_API_KEY', 'OLLAMA_API_KEY')
_SCANNED_ENVS: tuple[str, ...] = ALWAYS_SCANNED_ENVS


def scanned_credential_envs() -> tuple[str, ...]:
    """Env names `write_new` refuses to let into an output record.

    Derived, never guessed: the literals above, plus every `key_env` named by the
    material in use, plus whatever the transport itself treats as credential-bearing
    (`_secret_env_names`). A future material naming a third credential is scanned by
    construction rather than by coincidence.
    """
    return _SCANNED_ENVS


def register_credential_envs(material: dict | None = None) -> tuple[str, ...]:
    global _SCANNED_ENVS
    names = set(ALWAYS_SCANNED_ENVS)
    for endpoint in (material or {}).get('endpoints') or ():
        if isinstance(endpoint.get('key_env'), str) and endpoint['key_env']:
            names.add(endpoint['key_env'])
    try:
        names.update(_provider_module()._secret_env_names())
    except Exception:  # the transport is optional for pure-material operations
        pass
    _SCANNED_ENVS = tuple(sorted(names))
    return _SCANNED_ENVS


def write_new(path: Path, value: Any) -> None:
    """Write-once. An existing path is a custody failure, never an overwrite."""
    raw = value if isinstance(value, bytes) else encoded(value)
    for name in scanned_credential_envs():
        key = os.environ.get(name)
        if key and len(key) >= 8 and key.encode('utf-8') in raw:
            raise ValueError('CREDENTIAL_IN_OUTPUT')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


CODE_LIKE = re.compile('[A-Z0-9_]+')


def failure_code(exc: BaseException) -> str:
    """The declared failure code where there is one, else the exception class name.

    `ProviderFailure.code` is the transport's own stable code; a ValueError raised by
    this module carries its code as its whole message, by the convention `main` already
    reads. Anything else falls back to the class name.
    """
    code = getattr(exc, 'code', None)
    if isinstance(code, str) and code:
        return code
    text = str(exc)
    if CODE_LIKE.fullmatch(text):
        return text
    return type(exc).__name__


def assert_no_scoring_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ValueError('SCORING_KEY_FORBIDDEN')
            assert_no_scoring_keys(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_scoring_keys(item)


# ------------------------------------------------------- declared normalisation

def normalise_prose(text: str) -> str:
    """Declared prose content normalisation: word tokens only; layout is carrier."""
    lines = [BULLET.sub('', line) for line in text.splitlines()]
    return ' '.join(' '.join(lines).split())


def canonical_fcl(text: str) -> str:
    """Declared FCL-1 content normalisation: records as a set keyed by id; order is carrier."""
    doc = json.loads(text)
    out = dict(doc)
    out['records'] = sorted(doc['records'], key=lambda record: record['id'])
    if 'uptake' in doc:
        out['uptake'] = sorted(doc['uptake'])
    return json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


CONTRACTIONS = (("cannot", "can not"), ("Cannot", "Can not"),
                ("can't", "can not"), ("Can't", "Can not"),
                ("won't", "will not"), ("Won't", "Will not"),
                ("shan't", "shall not"), ("Shan't", "Shall not"),
                ("n't", " not"), ("'d", " would"), ("\u2019d", " would"),
                ("'ll", " will"), ("\u2019ll", " will"), ("'ve", " have"),
                ("'re", " are"), ("'m", " am"))


def expand_contractions(text: str) -> str:
    """Orthographic normalisation used only by the hedge-force count.

    "I'd" and "I would" are the same lexical items with the same modal force, so the
    count must not see a difference where there is none. Applied to original and
    recoded alike, so a quoted contraction reproduced verbatim cancels out.
    """
    for short, long in CONTRACTIONS:
        text = text.replace(short, long)
    return text


def marker_counts(text: str, markers: list[dict]) -> dict[str, int]:
    expanded = expand_contractions(text)
    out = {}
    for marker in markers:
        total = 0
        for token in marker['tokens']:
            total += len(re.findall(r'(?<![A-Za-z0-9_])' + re.escape(token) + r'(?![A-Za-z0-9_])',
                                    expanded, re.IGNORECASE))
        out[marker['family']] = total
    return out


QUOTE = re.compile(r'"[^"]*"|\u201c[^\u201d]*\u201d|(?<![A-Za-z])\'[^\']*\'(?![A-Za-z])')


def quoted_spans(text: str) -> list[str]:
    """Quoted material inside one unit, in order. A recoding reproduces it verbatim."""
    return QUOTE.findall(text)


def split_units(paragraph: str) -> list[str]:
    return SENTENCE.split(paragraph.strip())


def prose_shape(text: str) -> list[int]:
    return [len(split_units(p)) for p in text.split('\n\n')]


def join_prose(units: list[str], shape: list[int]) -> str:
    paragraphs, index = [], 0
    for count in shape:
        paragraphs.append(' '.join(units[index:index + count]))
        index += count
    return '\n\n'.join(paragraphs)


# ------------------------------------------------------------------ material

def validate_material(material: dict) -> dict:
    if material.get('schema') != SCHEMA_MATERIAL:
        raise ValueError('MATERIAL_SCHEMA')
    for name in ('system_common', 'public_contract', 'envelope', 'question', 'claim_ceiling',
                 'seed_policy', 'partial_delivery_rule'):
        if not isinstance(material.get(name), str) or not material[name].strip():
            raise ValueError('MATERIAL_TEXT')
    if not isinstance(material.get('envelope_unwrap'), dict):
        raise ValueError('MATERIAL_ENVELOPE_UNWRAP')
    rule = material.get('reading_rule')
    if not isinstance(rule, dict) or rule.get('schema') != 'minireason.c001.reading_rule.v1':
        raise ValueError('MATERIAL_READING_RULE')
    if [r.get('id') for r in rule.get('registers', ())] != ['T', 'E', 'D', 'G']:
        raise ValueError('MATERIAL_READING_RULE_REGISTERS')
    if list(rule.get('marks', ())) != ['differs', 'same', 'unresolved']:
        raise ValueError('MATERIAL_READING_RULE_MARKS')
    for name in ('preamble', 'replicate_baseline', 'order_of_reading', 'two_readers',
                 'never_aggregated'):
        if not isinstance(rule.get(name), str) or not rule[name].strip():
            raise ValueError('MATERIAL_READING_RULE')
    pins = material.get('transport_pins')
    if not isinstance(pins, dict):
        raise ValueError('MATERIAL_TRANSPORT_PINS')
    for name in ('module', 'module_sha256', 'registry', 'registry_sha256'):
        if not isinstance(pins.get(name), str) or not pins[name].strip():
            raise ValueError('MATERIAL_TRANSPORT_PINS')
    if list(material.get('cases', ())) != list(CASES):
        raise ValueError('MATERIAL_CASES')
    if material.get('replicates') != REPLICATES:
        raise ValueError('MATERIAL_REPLICATES')
    if sorted(material.get('arms', {})) != sorted(ARMS):
        raise ValueError('MATERIAL_ARMS')
    ceilings = material.get('ceilings', {})
    caps = ceilings.get('max_tokens')
    if not isinstance(caps, dict) or not caps:
        raise ValueError('MATERIAL_CEILINGS')
    if ceilings.get('max_tokens_authorised_maximum') != MAX_TOKENS_AUTHORISED:
        raise ValueError('MATERIAL_CEILINGS')
    if (not isinstance(ceilings.get('max_tokens_policy'), str)
            or not ceilings['max_tokens_policy'].strip()):
        raise ValueError('MATERIAL_CEILINGS')
    # The wall-clock timeout is a per-endpoint table exactly as max_tokens is, and the
    # two published places a reader may look - endpoints[].timeout_seconds and
    # ceilings.timeout_seconds - cannot be allowed to disagree.
    timeouts = ceilings.get('timeout_seconds')
    if not isinstance(timeouts, dict) or not timeouts:
        raise ValueError('MATERIAL_CEILINGS')
    if ceilings.get('timeout_seconds_authorised_maximum') != TIMEOUT_SECONDS_AUTHORISED:
        raise ValueError('MATERIAL_CEILINGS')
    if (not isinstance(ceilings.get('timeout_seconds_policy'), str)
            or not ceilings['timeout_seconds_policy'].strip()):
        raise ValueError('MATERIAL_CEILINGS')
    endpoints = material.get('endpoints')
    if not isinstance(endpoints, list) or len(endpoints) != ENDPOINT_COUNT:
        raise ValueError('MATERIAL_ENDPOINTS')
    slugs = set()
    for endpoint in endpoints:
        slug = endpoint.get('slug')
        if not isinstance(slug, str) or not SLUG_OK.fullmatch(slug) or slug in slugs:
            raise ValueError('MATERIAL_ENDPOINT_SLUG')
        for field in ('id', 'key_env', 'model', 'family'):
            if not isinstance(endpoint.get(field), str) or not endpoint[field]:
                raise ValueError('MATERIAL_ENDPOINT_FIELDS')
        if endpoint.get('honors_seed') not in (True, False, None):
            raise ValueError('MATERIAL_ENDPOINT_SEED')
        # max_tokens is declared per endpoint. It must be an integer inside the
        # authorised range AND agree with the `ceilings.max_tokens` table, so the two
        # published places a reader may look cannot disagree.
        cap = endpoint.get('max_tokens')
        if type(cap) is not int or not 1 <= cap <= MAX_TOKENS_AUTHORISED:
            raise ValueError('MATERIAL_ENDPOINT_MAX_TOKENS')
        if caps.get(endpoint['id']) != cap:
            raise ValueError('MATERIAL_ENDPOINT_MAX_TOKENS')
        # Same discipline for the timeout: an integer inside the transport's own
        # validation range, and the same value in both published tables.
        seconds = endpoint.get('timeout_seconds')
        if type(seconds) is not int or not 1 <= seconds <= TIMEOUT_SECONDS_AUTHORISED:
            raise ValueError('MATERIAL_ENDPOINT_TIMEOUT_SECONDS')
        if timeouts.get(endpoint['id']) != seconds:
            raise ValueError('MATERIAL_ENDPOINT_TIMEOUT_SECONDS')
        slugs.add(slug)
    if sorted(caps) != sorted(e['id'] for e in endpoints):
        raise ValueError('MATERIAL_CEILINGS')
    if sorted(timeouts) != sorted(e['id'] for e in endpoints):
        raise ValueError('MATERIAL_CEILINGS')
    # V2: the OPTIONAL dispatch scope. Absent, the material is an unrestricted C001
    # material and every check below is a no-op, so a v1 material validates here exactly
    # as it validates under v1. Present, it must name declared endpoint ids and declared
    # arms, must not be empty on either axis, must not repeat an entry (a repeat would
    # silently double a coordinate), must carry its own stated reason, and must agree
    # with the material's own `planned_calls`. Narrowing the scope is a ceiling-class
    # change: it moves the material, hence the plan_id, hence the claim (PLAN section 13).
    scope = material.get('dispatch_scope')
    if scope is not None:
        if not isinstance(scope, dict):
            raise ValueError('MATERIAL_DISPATCH_SCOPE')
        if sorted(scope) != ['arms', 'endpoints', 'reason']:
            raise ValueError('MATERIAL_DISPATCH_SCOPE')
        if not isinstance(scope.get('reason'), str) or not scope['reason'].strip():
            raise ValueError('MATERIAL_DISPATCH_SCOPE')
        declared = [e['id'] for e in endpoints]
        chosen = scope.get('endpoints')
        if (not isinstance(chosen, list) or not chosen
                or len(set(chosen)) != len(chosen)
                or any(name not in declared for name in chosen)):
            raise ValueError('MATERIAL_DISPATCH_SCOPE_ENDPOINTS')
        arms = scope.get('arms')
        if (not isinstance(arms, list) or not arms
                or len(set(arms)) != len(arms)
                or any(arm not in ARMS for arm in arms)):
            raise ValueError('MATERIAL_DISPATCH_SCOPE_ARMS')
    if material.get('planned_calls') != planned_call_count(material):
        raise ValueError('MATERIAL_PLANNED_CALLS')
    if (ceilings.get('automatic_retries') != AUTOMATIC_RETRIES
            or ceilings.get('max_concurrent_per_key') != MAX_CONCURRENT_PER_KEY
            or ceilings.get('temperature') != 'provider-default'):
        raise ValueError('MATERIAL_CEILINGS')
    for arm in ARMS:
        block = material['arms'][arm]
        if sorted(block.get('cases', {})) != sorted(CASES):
            raise ValueError('MATERIAL_ARM_CASES')
        for name in ('account', 'rival'):
            if not isinstance(block['frozen_inputs'][name].get('projection'), str):
                raise ValueError('MATERIAL_FROZEN_INPUT')
        addresses = block.get('artifact_addresses')
        if not isinstance(addresses, dict):
            raise ValueError('MATERIAL_ARTIFACT_ADDRESSES')
        for name in ('objection', 'account', 'rival'):
            value = addresses.get(name)
            if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
                raise ValueError('MATERIAL_ARTIFACT_ADDRESSES')
            if value != (block['objection_source'] if name == 'objection'
                         else block['frozen_inputs'][name])['artifact_id']:
                raise ValueError('MATERIAL_ARTIFACT_ADDRESS_DISAGREES')
        if addresses.get('truncation_chars') != 16:
            raise ValueError('MATERIAL_ARTIFACT_ADDRESSES')
        if len({addresses[n] for n in ('objection', 'account', 'rival')}) != 3:
            raise ValueError('MATERIAL_ARTIFACT_ADDRESSES_NOT_DISTINCT')
    register_credential_envs(material)
    return material


def check_material_integrity(material: dict, repo: Path) -> dict:
    """Every source pin re-read from the tree it names. A missing tree is a failure."""
    repo = Path(repo)
    checked = {}
    for name, expected in material['source_pins'].items():
        if '..' in Path(name).parts or Path(name).is_absolute():
            raise ValueError('SOURCE_PIN_OUTSIDE_REPOSITORY')
        path = repo / name
        if not path.exists():
            raise ValueError('SOURCE_PIN_MISSING')
        if sha(path.read_bytes()) != expected:
            raise ValueError('SOURCE_PIN_MISMATCH')
        checked[name] = expected
    for arm in ARMS:
        block = material['arms'][arm]
        source = block['objection_source']
        artifact = load(repo / source['source_path'])
        if (artifact['artifact_id'] != source['artifact_id']
                or artifact['body_sha256'] != source['body_sha256']
                or artifact['commitments_sha256'] != source['commitments_sha256']
                or artifact['public_text_sha256'] != source['public_text_sha256']
                or artifact['coordinate'] != source['coordinate']):
            raise ValueError('OBJECTION_ARTIFACT_MISMATCH')
        original = block['cases']['original']
        if (original['body'] != artifact['body']
                or original['commitments'] != artifact['commitments']
                or tsha(original['body']) != artifact['body_sha256']
                or tsha(original['commitments']) != artifact['commitments_sha256']):
            raise ValueError('ORIGINAL_CASE_NOT_THE_OCCURRENCE_BYTES')
        for name in ('account', 'rival'):
            frozen = block['frozen_inputs'][name]
            other = load(repo / frozen['source_path'])
            if (other['artifact_id'] != frozen['artifact_id']
                    or other['body_sha256'] != frozen['body_sha256']
                    or other['commitments_sha256'] != frozen['commitments_sha256']):
                raise ValueError('FROZEN_INPUT_ARTIFACT_MISMATCH')
    return checked


def check_transport_pins(material: dict) -> dict:
    """Re-hash the transport module and the endpoint registry it supplies.

    Neither file lives in the pinned repository tree, so `check_material_integrity`
    cannot reach them; both supply parts of the effective configuration (base_url,
    chat_path, timeout_seconds, max_concurrency) that `plan.json` would otherwise
    not cover. Re-hashed by prepare, verify, run, audit and table.
    """
    pins = material['transport_pins']
    module = _provider_module()
    module_path = Path(module.__file__).resolve()
    registry_path = module_path.parent / 'data' / 'endpoints.json'
    if not registry_path.exists():
        raise ValueError('TRANSPORT_PIN_MISSING')
    observed = {'module_sha256': sha(module_path.read_bytes()),
                'registry_sha256': sha(registry_path.read_bytes())}
    if (observed['module_sha256'] != pins['module_sha256']
            or observed['registry_sha256'] != pins['registry_sha256']):
        raise ValueError('TRANSPORT_PIN_MISMATCH')
    return {'module': pins['module'], 'registry': pins['registry'],
            'resolved_from': str(module_path.parent.parent), **observed}


def check_recoding(material: dict) -> dict:
    """Every original unit mapped; the recoded document reconstructs from the table alone."""
    report = {}
    for arm in ARMS:
        block = material['arms'][arm]
        original, recoded = block['cases']['original'], block['cases']['recoding']
        units = block['recoding']['units']
        if len(units) != block['recoding']['unit_count']:
            raise ValueError('RECODING_UNIT_COUNT')
        declared = block['recoding'].get('rule')
        if not isinstance(declared, dict) or not declared:
            raise ValueError('RECODING_RULE_SET')
        markers = block['recoding'].get('hedge_markers')
        if not isinstance(markers, list) or not markers:
            raise ValueError('RECODING_HEDGE_MARKERS_NOT_DECLARED')
        for marker in markers:
            if (not isinstance(marker, dict) or not isinstance(marker.get('family'), str)
                    or not isinstance(marker.get('tokens'), list) or not marker['tokens']):
                raise ValueError('RECODING_HEDGE_MARKERS_NOT_DECLARED')
        seen, hedge_checked, rules_used = set(), 0, set()
        for unit in units:
            for field in ('unit_id', 'location', 'original', 'recoded'):
                if not isinstance(unit.get(field), str) or not unit[field].strip():
                    raise ValueError('RECODING_UNIT_FIELD')
            if not isinstance(unit.get('rules'), list) or not unit['rules']:
                raise ValueError('RECODING_UNIT_RULES')
            # (c) every declared label of every unit is a member of the declared rule set.
            if not set(unit['rules']) <= set(declared):
                raise ValueError('RECODING_UNDECLARED_RULE')
            rules_used.update(unit['rules'])
            if unit['unit_id'] in seen:
                raise ValueError('RECODING_DUPLICATE_UNIT')
            seen.add(unit['unit_id'])
            # (b) hedge force, mechanically: every declared marker family is preserved
            # in count inside the unit, after contraction expansion.
            before = marker_counts(unit['original'], markers)
            after = marker_counts(unit['recoded'], markers)
            if before != after:
                raise ValueError('RECODING_HEDGE_FORCE_CHANGED')
            hedge_checked += 1
            # quoted material is reproduced verbatim, so a recoding cannot rewrite what
            # the objection quotes from the account or from the problem statement.
            if quoted_spans(unit['original']) != quoted_spans(unit['recoded']):
                raise ValueError('RECODING_QUOTATION_CHANGED')

        body_units = [u for u in units if u['location'] == 'B']
        shape = prose_shape(original['body'])
        if join_prose([u['original'] for u in body_units], shape) != original['body']:
            raise ValueError('RECODING_BODY_ORIGINAL_NOT_COVERED')
        if join_prose([u['recoded'] for u in body_units], shape) != recoded['body']:
            raise ValueError('RECODING_BODY_NOT_RECONSTRUCTIBLE')

        if arm == 'fcl':
            source = json.loads(original['commitments'])
            target = json.loads(recoded['commitments'])
            mapped = {u['unit_id']: u for u in units if u['location'].startswith('commitments/')}
            expected, rebuilt_source, rebuilt_target = set(), {}, {}
            for record in source['records']:
                for field, value in record.items():
                    if field in ('id', 'type') or not isinstance(value, str):
                        continue
                    ids = [f'K.{record["id"]}.{field}.S{i + 1}'
                           for i in range(len(split_units(value)))]
                    expected.update(ids)
                    rebuilt_source[(record['id'], field)] = ' '.join(
                        mapped[i]['original'] for i in ids if i in mapped)
                    rebuilt_target[(record['id'], field)] = ' '.join(
                        mapped[i]['recoded'] for i in ids if i in mapped)
            if expected != set(mapped):
                raise ValueError('RECODING_COMMITMENT_UNITS_INCOMPLETE')
            for record in source['records']:
                for field, value in record.items():
                    if field in ('id', 'type') or not isinstance(value, str):
                        continue
                    if rebuilt_source[(record['id'], field)] != value:
                        raise ValueError('RECODING_COMMITMENT_ORIGINAL_NOT_COVERED')
            for record in target['records']:
                for field, value in record.items():
                    if field in ('id', 'type') or not isinstance(value, str):
                        continue
                    if rebuilt_target[(record['id'], field)] != value:
                        raise ValueError('RECODING_COMMITMENT_NOT_RECONSTRUCTIBLE')
            # (a) every FCL-1 record's id, type, reference arrays and the document's
            # uptake list are unchanged by the recoding, checked record by record so the
            # refusal names which record moved rather than only that something did.
            before_records = {r['id']: r for r in source['records']}
            after_records = {r['id']: r for r in target['records']}
            if sorted(before_records) != sorted(after_records):
                raise ValueError('RECODING_CHANGED_FCL_RECORD_IDS')
            for rid, record in before_records.items():
                other = after_records[rid]
                if record.get('type') != other.get('type'):
                    raise ValueError('RECODING_CHANGED_FCL_RECORD_TYPE')
                if sorted(record) != sorted(other):
                    raise ValueError('RECODING_CHANGED_FCL_RECORD_FIELDS')
                for field in FCL_REF_FIELDS:
                    if list(record.get(field) or ()) != list(other.get(field) or ()):
                        raise ValueError('RECODING_CHANGED_FCL_REFERENCES')
                for field, value in record.items():
                    if not isinstance(value, str) and record.get(field) != other.get(field):
                        raise ValueError('RECODING_CHANGED_FCL_NON_STRING_FIELD')
            if list(source.get('uptake') or ()) != list(target.get('uptake') or ()):
                raise ValueError('RECODING_CHANGED_FCL_UPTAKE')
            if source.get('language') != target.get('language'):
                raise ValueError('RECODING_CHANGED_FCL_LANGUAGE')
            if fcl_structure(original['commitments']) != fcl_structure(recoded['commitments']):
                raise ValueError('RECODING_CHANGED_FCL_STRUCTURE')
        else:
            commitment_units = [u for u in units if u['location'] == 'C']
            shape = prose_shape(original['commitments'])
            if join_prose([u['original'] for u in commitment_units], shape) != original['commitments']:
                raise ValueError('RECODING_COMMITMENT_ORIGINAL_NOT_COVERED')
            if join_prose([u['recoded'] for u in commitment_units], shape) != recoded['commitments']:
                raise ValueError('RECODING_COMMITMENT_NOT_RECONSTRUCTIBLE')

        if normalise_prose(recoded['body']) == normalise_prose(original['body']):
            raise ValueError('RECODING_IS_IDENTITY')
        report[arm] = {'units': len(units), 'every_original_unit_mapped': True,
                       'recoded_document_reconstructible_from_table': True,
                       'hedge_marker_families': len(markers),
                       'units_hedge_checked': hedge_checked,
                       'rule_labels_declared': sorted(declared),
                       'rule_labels_used': sorted(rules_used),
                       'rule_labels_declared_and_not_used': sorted(set(declared) - rules_used)}
    return report


def check_carrier(material: dict) -> dict:
    """Content tokens identical after the declared normalisation; bytes not identical."""
    report = {}
    for arm in ARMS:
        block = material['arms'][arm]
        original, carrier = block['cases']['original'], block['cases']['carrier']
        if normalise_prose(original['body']) != normalise_prose(carrier['body']):
            raise ValueError('CARRIER_BODY_CONTENT_CHANGED')
        if arm == 'fcl':
            same = canonical_fcl(original['commitments']) == canonical_fcl(carrier['commitments'])
        else:
            same = normalise_prose(original['commitments']) == normalise_prose(carrier['commitments'])
        if not same:
            raise ValueError('CARRIER_COMMITMENTS_CONTENT_CHANGED')
        if original['body'] == carrier['body'] and original['commitments'] == carrier['commitments']:
            raise ValueError('CARRIER_NOT_DISTURBED')
        proof = block['carrier']['proof']
        if not (proof.get('body_equal') and proof.get('commitments_equal')
                and proof.get('body_bytes_differ') and proof.get('commitments_bytes_differ')):
            raise ValueError('CARRIER_PROOF_DISAGREES')
        report[arm] = {'content_tokens_identical': True, 'bytes_differ': True}
    return report


def check_control(material: dict) -> dict:
    """The control carries no objection content, and differs from ORIGINAL only in that block."""
    report = {}
    absent = 'Source objection: absent in the first template invocation; selected view both.'
    for arm in ARMS:
        block = material['arms'][arm]
        control = block['cases']['control']['objection_projection']
        if control != absent:
            raise ValueError('CONTROL_WORDING_NOT_THE_RUNNER_ABSENT_WORDING')
        original_brief = brief_for(material, arm, 'original')
        control_brief = brief_for(material, arm, 'control')
        if original_brief.replace(
                block['cases']['original']['objection_projection'], control, 1) != control_brief:
            raise ValueError('CONTROL_DIFFERS_OUTSIDE_THE_OBJECTION_BLOCK')
        # Both sides of this test are substring tests over the same normalisation, so a
        # token glued to punctuation cannot make a shared phrase look like a leak.
        frozen_regions = normalise_prose(
            material['node']['instruction'] + ' ' + material['problem']['prose'] + ' '
            + block['frozen_inputs']['account']['projection'] + ' '
            + block['frozen_inputs']['rival']['projection'] + ' ' + material['envelope'])
        haystack = normalise_prose(control_brief)
        leaked, shared = 0, 0
        for text in (block['cases']['original']['body'],
                     block['cases']['original']['commitments']):
            tokens = normalise_prose(text).split()
            for i in range(len(tokens) - 5):
                shingle = ' '.join(tokens[i:i + 6])
                if shingle not in haystack:
                    continue
                # A phrase the objection shares with the account or the rival reaches the
                # node identically in all four cases, so it cannot differentiate them. It is
                # recorded, not treated as a control failure.
                if shingle in frozen_regions:
                    shared += 1
                else:
                    leaked += 1
        if leaked:
            raise ValueError('CONTROL_CARRIES_OBJECTION_CONTENT')
        report[arm] = {'objection_block_is_the_runner_absent_wording': True,
                       'objection_shingles_leaked': 0,
                       'objection_shingles_also_present_in_frozen_inputs': shared}
    return report


# ------------------------------------------------------------------ rendering

def brief_for(material: dict, arm: str, case: str) -> str:
    """The user message. Reproduces `render_node`'s direct_explicit_views branch."""
    if arm not in ARMS or case not in CASES:
        raise ValueError('UNKNOWN_ARM_OR_CASE')
    block = material['arms'][arm]
    node = material['node']
    parts = ['## Node ' + node['node_id'], node['instruction'],
             '## Original problem', material['problem']['prose']]
    for binding in node['inputs']:
        source = binding['source']
        projection = (block['cases'][case]['objection_projection'] if source == 'objection'
                      else block['frozen_inputs'][source]['projection'])
        parts.extend(['## Selected input ' + source, projection])
    parts.append(material['envelope'])
    return '\n\n'.join(parts)


def messages_for(material: dict, arm: str, case: str) -> list[dict[str, str]]:
    system = (material['system_common'] + '\n\n' + material['policies'][arm]
              + '\n\n' + material['public_contract'])
    return [{'role': 'system', 'content': system},
            {'role': 'user', 'content': brief_for(material, arm, case)}]


def shared_envelope(material: dict, arm: str) -> tuple[str, str]:
    """The bytes every case of one arm shares. The Appendix-B-14 guarantee, mechanically."""
    block = material['arms'][arm]
    marker = block['cases']['original']['objection_projection']
    brief = brief_for(material, arm, 'original')
    if brief.count(marker) != 1:
        raise ValueError('OBJECTION_BLOCK_NOT_LOCATED')
    head, _, tail = brief.partition(marker)
    for case in CASES:
        projection = block['cases'][case]['objection_projection']
        if brief_for(material, arm, case) != head + projection + tail:
            raise ValueError('SHARED_ENVELOPE_MISMATCH')
    return head, tail


def payload_for(messages: list[dict[str, str]], spec: dict) -> dict:
    """The exact payload OpenAICompatProvider builds for a non-native endpoint.

    `temperature` is never sent, so the provider default applies; `seed` appears
    only where the seed policy sends one.
    """
    payload = {'model': spec['model'], 'messages': [dict(m) for m in messages],
               'stream': False, 'max_tokens': spec['max_tokens'],
               'response_format': {'type': 'json_object'}}
    if spec.get('seed') is not None:
        payload['seed'] = spec['seed']
    return payload


# ------------------------------------------------------------------ coordinates

def coordinate(endpoint_slug: str, arm: str, case: str, replicate: int) -> dict:
    if not SLUG_OK.fullmatch(endpoint_slug) or arm not in ARMS or case not in CASES:
        raise ValueError('INVALID_COORDINATE')
    if type(replicate) is not int or not 1 <= replicate <= REPLICATES:
        raise ValueError('INVALID_COORDINATE')
    return {'endpoint_slug': endpoint_slug, 'arm': arm, 'case': case, 'replicate': replicate}


def label(coord: dict) -> str:
    return f'{coord["endpoint_slug"]}/{coord["arm"]}/{coord["case"]}/rep{coord["replicate"]}'


def at(output: Path, category: str, coord: dict, suffix: str = 'json') -> Path:
    if not SLUG_OK.fullmatch(category) or not SLUG_OK.fullmatch(suffix):
        raise ValueError('INVALID_CATEGORY')
    coord = coordinate(coord['endpoint_slug'], coord['arm'], coord['case'], coord['replicate'])
    name = f'rep{coord["replicate"]}'
    if not REP_OK.fullmatch(name):
        raise ValueError('INVALID_REPLICATE')
    return (Path(output) / category / coord['endpoint_slug'] / coord['arm'] /
            coord['case'] / (name + '.' + suffix))


def provider_dir(output: Path, coord: dict) -> Path:
    return at(output, 'provider', coord).with_suffix('')


# V2: the three scope readers. Each answers the unrestricted question when the material
# declares no `dispatch_scope`, so every caller behaves as v1 on a v1 material.
def scoped_endpoints(material: dict) -> list[dict]:
    """V2: the endpoint entries this occurrence dispatches, in the material's own order."""
    scope = material.get('dispatch_scope')
    if not scope:
        return list(material['endpoints'])
    chosen = set(scope['endpoints'])
    return [e for e in material['endpoints'] if e['id'] in chosen]


def scoped_arms(material: dict) -> tuple[str, ...]:
    """V2: the arms this occurrence dispatches, in ARMS order (never the caller's)."""
    scope = material.get('dispatch_scope')
    if not scope:
        return tuple(ARMS)
    chosen = set(scope['arms'])
    return tuple(arm for arm in ARMS if arm in chosen)


def planned_call_count(material: dict) -> int:
    """V2: cases x replicates x scoped endpoints x scoped arms; PLANNED_CALLS unscoped."""
    return (len(CASES) * REPLICATES
            * len(scoped_endpoints(material)) * len(scoped_arms(material)))


def all_coordinates(material: dict) -> list[dict]:
    # V2: built over the dispatch scope rather than over every declared endpoint and both
    # arms. The iteration order is unchanged -- endpoint-major, then arm, case, replicate
    # -- so a scoped plan's coordinate list is the v1 list with the out-of-scope
    # coordinates removed, in place, and `build_waves` groups it exactly as before.
    return [coordinate(endpoint['slug'], arm, case, replicate)
            for endpoint in scoped_endpoints(material)
            for arm in scoped_arms(material) for case in CASES
            for replicate in range(1, REPLICATES + 1)]


# ------------------------------------------------------------------ plan

def plan_body(material: dict, material_raw: bytes, helper_raw: bytes) -> dict:
    briefs = {}
    for arm in ARMS:
        head, tail = shared_envelope(material, arm)
        briefs[arm] = {
            'shared_prefix_sha256': tsha(head), 'shared_suffix_sha256': tsha(tail),
            'shared_prefix_chars': len(head), 'shared_suffix_chars': len(tail),
            'cases': {case: {'brief_sha256': tsha(brief_for(material, arm, case)),
                             'messages_sha256': digest(messages_for(material, arm, case)),
                             'objection_projection_sha256':
                                 tsha(material['arms'][arm]['cases'][case]['objection_projection'])}
                      for case in CASES}}
    coordinates = all_coordinates(material)
    # V2: the planned count is the scoped count. On a material with no `dispatch_scope`
    # `planned_call_count` returns PLANNED_CALLS, so this is v1's own check.
    planned = planned_call_count(material)
    if len(coordinates) != planned:
        raise ValueError('PLANNED_CALL_COUNT')
    return {
        'schema': 'minireason.c001.plan.v1',
        'study': material['study'],
        'question': material['question'],
        'claim_ceiling': material['claim_ceiling'],
        'material_sha256': sha(material_raw),
        'helper_sha256': sha(helper_raw),
        'source_pins': material['source_pins'],
        'transport_pins': material['transport_pins'],
        'reading_rule': material['reading_rule'],
        'node': {'template_id': material['node']['template_id'],
                 'node_id': material['node']['node_id'],
                 'instruction_sha256': material['node']['instruction_sha256'],
                 'varying_input': material['node']['varying_input'],
                 'frozen_inputs': material['node']['frozen_inputs']},
        'arms': list(ARMS), 'cases': list(CASES), 'replicates': REPLICATES,
        'seeds': material['seeds'], 'seed_policy': material['seed_policy'],
        'envelope_unwrap': material['envelope_unwrap'],
        'partial_delivery_rule': material['partial_delivery_rule'],
        'endpoints': [{'id': e['id'], 'slug': e['slug'], 'model': e['model'],
                       'key_env': e['key_env'], 'family': e['family'],
                       'honors_seed': e['honors_seed'],
                       'max_tokens': e['max_tokens'],
                       'timeout_seconds': e['timeout_seconds']}
                      for e in material['endpoints']],
        'ceilings': material['ceilings'],
        'briefs': briefs,
        'planned_calls': planned,
        # V2: the scope is frozen into the plan ONLY when the material declares one, so a
        # plan built from a v1 material has no such key and is v1's plan field for field.
        # Where it is present it is inside `plan_id`: an occurrence cannot quietly widen
        # or narrow what it dispatches without minting a different identity.
        **({'dispatch_scope': material['dispatch_scope']}
           if material.get('dispatch_scope') else {}),
        'coordinates': coordinates,
        'record_layout': {
            'brief': 'briefs/<arm>/<case>.json',
            'request': 'requests/<endpoint_slug>/<arm>/<case>/rep<N>.json',
            'attempt': 'attempts/<endpoint_slug>/<arm>/<case>/rep<N>.json',
            'response': 'responses/<endpoint_slug>/<arm>/<case>/rep<N>.json (+ .txt, raw bytes)',
            'artifact': 'artifacts/<endpoint_slug>/<arm>/<case>/rep<N>.json',
            'provider': 'provider/<endpoint_slug>/<arm>/<case>/rep<N>/call-0001.{request,response}.json'},
        'determinism': 'No wall clock enters plan_id, any request digest or any artifact digest.'}


def prepare(material_path: Path, output: Path, repo: Path,
            *, offline_provider_factory: Callable[[dict, Path], Any] | None = None) -> dict:
    material_raw = Path(material_path).read_bytes()
    material = validate_material(json.loads(material_raw))
    integrity = check_material_integrity(material, repo)
    transport = check_transport_pins(material)
    recoding = check_recoding(material)
    carrier = check_carrier(material)
    control = check_control(material)

    plan = plan_body(material, material_raw, Path(__file__).read_bytes())
    plan['plan_id'] = digest(plan)
    preflight = offline_preflight(material, plan, factory=offline_provider_factory)

    output = Path(output)
    write_new(output / 'material.json', material_raw)
    for arm in ARMS:
        for case in CASES:
            messages = messages_for(material, arm, case)
            write_new(output / 'briefs' / arm / (case + '.json'),
                      {'schema': 'minireason.c001.brief.v1', 'arm': arm, 'case': case,
                       'plan_id': plan['plan_id'], 'messages': messages,
                       'messages_sha256': digest(messages),
                       'brief_sha256': tsha(brief_for(material, arm, case))})
    write_new(output / 'plan.json', plan)
    write_new(output / 'preflight.json',
              {'schema': 'minireason.c001.preflight.v1', 'plan_id': plan['plan_id'],
               'source_pins_verified': integrity, 'transport_pins_verified': transport,
               'credential_envs_scanned': list(scanned_credential_envs()),
               'recoding': recoding, 'carrier': carrier,
               'control': control, **preflight})
    write_new(output / 'RECODING_TABLE.md', render_recoding_table(material).encode('utf-8'))
    return {'plan_id': plan['plan_id'], 'planned_calls': plan['planned_calls'],
            'provider_calls': preflight['provider_calls']}


def offline_preflight(material: dict, plan: dict,
                      *, factory: Callable[[dict], Any] | None = None) -> dict:
    """Build every planned call THROUGH an OfflineProvider and never complete one.

    The provider is not merely constructed and set aside: each coordinate's payload is
    built by the provider's own `_build_payload`, through its own argument validation
    and its own JSON-mode prompt check, and compared against this driver's
    `payload_for`. So the preflight exercises the code path the live call will take,
    the offline script is left empty (any actual `complete()` would raise
    TRANSPORT_OR_RESPONSE_ERROR), and the `provider_calls == 0` assertion reads a
    counter that this loop could actually move.
    """
    import tempfile
    with tempfile.TemporaryDirectory(prefix='c001-preflight-') as records_root:
        return _offline_preflight(material, plan, factory, Path(records_root))


def _offline_preflight(material: dict, plan: dict, factory, records_root: Path) -> dict:
    factory = factory or _offline_provider
    providers, source = {}, None
    for endpoint in material['endpoints']:
        provider, source = factory(endpoint, records_root)
        providers[endpoint['slug']] = provider
    planned, seen, built = 0, {}, 0
    response_format = {'type': 'json_object'}
    # The ceiling each payload must carry, read back from the FROZEN plan rather than
    # from the material, so a payload built with some other ceiling is caught even when
    # the material and the plan have drifted apart.
    planned_caps = {e['slug']: e['max_tokens'] for e in plan['endpoints']}
    planned_timeouts = {e['slug']: e['timeout_seconds'] for e in plan['endpoints']}
    for coord in plan['coordinates']:
        endpoint = next(e for e in material['endpoints'] if e['slug'] == coord['endpoint_slug'])
        provider = providers[coord['endpoint_slug']]
        spec = spec_for(endpoint, coord)
        messages = messages_for(material, coord['arm'], coord['case'])
        payload = payload_for(messages, spec)
        key = (coord['arm'], coord['case'])
        seen.setdefault(key, digest(messages))
        if seen[key] != digest(messages):
            raise ValueError('BRIEF_NOT_STABLE_ACROSS_ENDPOINTS')
        frozen = plan['briefs'][coord['arm']]['cases'][coord['case']]
        if digest(messages) != frozen['messages_sha256']:
            raise ValueError('BRIEF_DIGEST_MISMATCH')
        planned_cap = planned_caps.get(coord['endpoint_slug'])
        if (payload['max_tokens'] != planned_cap
                or payload['max_tokens'] != endpoint['max_tokens']
                or not 1 <= payload['max_tokens'] <= MAX_TOKENS_AUTHORISED
                or payload['response_format'] != response_format):
            raise ValueError('CEILING_NOT_APPLIED')
        if 'temperature' in payload:
            raise ValueError('TEMPERATURE_MUST_BE_PROVIDER_DEFAULT')
        provider._validate_call_args(max_tokens=spec['max_tokens'],
                                     reasoning_effort='high', extra=None)
        provider._check_json_mode_prompt(messages, response_format)
        provider_payload = provider._build_payload(
            messages, response_format=response_format, max_tokens=spec['max_tokens'],
            temperature=None, seed=spec['seed'], thinking=None,
            reasoning_effort='high', extra=None)
        settings = provider._settings_view(
            max_tokens=spec['max_tokens'], temperature=None, seed=spec['seed'],
            response_format=dict(response_format), thinking=None, reasoning_effort=None,
            extra={}, offline=True)
        # The timeout the TRANSPORT will actually use, read back off the provider this
        # driver constructed, against the value frozen in the plan. `_settings_view`
        # reports `self.endpoint.timeout_seconds`, so this reads the replaced Endpoint
        # and fails if `dataclasses.replace` did not reach the object that holds the
        # socket. Any disagreement between the plan, the material, the spec and the
        # transport is one code: TIMEOUT_NOT_APPLIED.
        planned_timeout = planned_timeouts.get(coord['endpoint_slug'])
        if (type(planned_timeout) is not int
                or not 1 <= planned_timeout <= TIMEOUT_SECONDS_AUTHORISED
                or endpoint['timeout_seconds'] != planned_timeout
                or spec['timeout_seconds'] != planned_timeout
                or settings.get('timeout_seconds') != planned_timeout):
            raise ValueError('TIMEOUT_NOT_APPLIED')
        if settings.get('max_concurrency', 0) > MAX_CONCURRENT_PER_KEY:
            raise ValueError('ENDPOINT_CONCURRENCY_ABOVE_AUTHORISATION')
        if digest(provider_payload) != digest(payload):
            raise ValueError('PAYLOAD_NOT_THE_TRANSPORTS')
        built += 1
        planned += 1
    calls = sum(p.calls for p in providers.values())
    # V2: checked against the plan's own frozen `planned_calls` rather than the module
    # constant, so the preflight builds every planned payload of a scoped occurrence and
    # no more. `plan_body` already refused unless that number is the scoped count.
    expected = plan['planned_calls']
    if planned != expected or built != expected:
        raise ValueError('PLANNED_CALL_COUNT')
    if calls != 0:
        raise ValueError('OFFLINE_PREFLIGHT_MADE_A_PROVIDER_CALL')
    return {'planned_calls': planned, 'provider_calls': calls,
            'payloads_built_by_the_transport': built,
            'distinct_message_pairs': len(seen), 'offline_provider': source,
            'status': 'OFFLINE_PREFLIGHT_PASSED'}


def verify(output: Path, repo: Path | None) -> tuple[dict, dict]:
    output = Path(output)
    material_raw = (output / 'material.json').read_bytes()
    material = validate_material(json.loads(material_raw))
    expected = plan_body(material, material_raw, Path(__file__).read_bytes())
    expected['plan_id'] = digest(expected)
    if load(output / 'plan.json') != expected:
        raise ValueError('IMMUTABLE_PLAN_MISMATCH')
    check_transport_pins(material)
    if repo is not None:
        check_material_integrity(material, repo)
    return material, expected


# ------------------------------------------------------------------ transport

def _provider_module():
    extra = os.environ.get('MINIREASON_PROVIDER_SRC')
    if extra and extra not in sys.path:
        sys.path.insert(0, extra)
    from minireason import provider_openai_compat as module  # noqa: PLC0415
    return module


def _offline_provider(endpoint: dict, records_root: Path) -> tuple[Any, str]:
    """One OfflineProvider per endpoint, under the caller's single temporary root.

    The script is empty on purpose: the preflight builds payloads through this
    provider but never completes a call, and an accidental `complete()` raises
    rather than passing silently.
    """
    module = _provider_module()
    return (module.OfflineProvider(resolve_endpoint(endpoint),
                                   Path(records_root) / endpoint['slug'], []),
            'minireason.provider_openai_compat.OfflineProvider')


def resolve_endpoint(endpoint: dict) -> Any:
    """The registry Endpoint, with this study's declared per-endpoint timeout applied.

    `endpoints.json` is a PUBLISHED, PINNED file that other studies' plans pin too, so
    C001 never edits it: the declared `timeout_seconds` is applied here, to the resolved
    `Endpoint` value, by `dataclasses.replace`. The replacement re-runs the dataclass's
    own `__post_init__`, so a value outside the transport's 1..600 range is refused by
    the transport itself rather than by this driver's opinion of it; the result is then
    re-read and must carry exactly the declared value (`TIMEOUT_NOT_APPLIED`).

    Every provider this driver constructs - live and offline - passes through here, so
    there is no path by which a call reaches the wire under the registry's own 180 s.
    """
    module = _provider_module()
    resolved = module.ENDPOINTS.get(endpoint['id'])
    if resolved is None:
        raise ValueError('ENDPOINT_NOT_IN_REGISTRY')
    if resolved.model != endpoint['model'] or resolved.key_env != endpoint['key_env']:
        raise ValueError('ENDPOINT_REGISTRY_DISAGREES_WITH_MATERIAL')
    if resolved.native:
        raise ValueError('ENDPOINT_MUST_BE_THE_OPENAI_COMPATIBLE_VARIANT')
    if resolved.max_concurrency > MAX_CONCURRENT_PER_KEY:
        raise ValueError('ENDPOINT_CONCURRENCY_ABOVE_AUTHORISATION')
    seconds = endpoint.get('timeout_seconds')
    if type(seconds) is not int or not 1 <= seconds <= TIMEOUT_SECONDS_AUTHORISED:
        raise ValueError('TIMEOUT_NOT_APPLIED')
    applied = dataclasses.replace(resolved, timeout_seconds=seconds)
    if applied.timeout_seconds != seconds:
        raise ValueError('TIMEOUT_NOT_APPLIED')
    # Everything else must be the registry's own bytes: the replacement changes the
    # timeout and nothing else.
    if dataclasses.replace(applied, timeout_seconds=resolved.timeout_seconds) != resolved:
        raise ValueError('TIMEOUT_REPLACEMENT_CHANGED_MORE_THAN_THE_TIMEOUT')
    return applied


def live_provider(endpoint: dict, records: Path) -> Any:
    module = _provider_module()
    return module.OpenAICompatProvider(resolve_endpoint(endpoint), Path(records))


def spec_for(endpoint: dict, coord: dict) -> dict:
    """The full effective call configuration for one coordinate.

    Seed policy: send seed=<replicate> unless the endpoint declares honors_seed false.
    A null honors_seed means unverified: the seed is sent and its effect is recorded
    as unestablished rather than assumed.
    """
    honors = endpoint.get('honors_seed')
    seed = None if honors is False else coord['replicate']
    return {'endpoint_id': endpoint['id'], 'endpoint_slug': endpoint['slug'],
            'model': endpoint['model'], 'key_env': endpoint['key_env'],
            'family': endpoint['family'],
            'max_tokens': endpoint['max_tokens'],
            # Declared per endpoint and applied to the registry Endpoint by
            # `dataclasses.replace` in `resolve_endpoint`; recorded in every request.
            'timeout_seconds': endpoint['timeout_seconds'],
            'timeout_seconds_registry_default': TIMEOUT_SECONDS_REGISTRY_DEFAULT,
            'temperature': 'provider-default', 'response_format': {'type': 'json_object'},
            'automatic_retries': AUTOMATIC_RETRIES,
            'seed': seed, 'seed_requested': coord['replicate'], 'honors_seed': honors,
            'native_reasoning': ('not manipulated; endpoint default. Reasoning tokens count '
                                 'against max_tokens and reasoning text is never persisted.')}


# ------------------------------------------------------------------ decoding

def _envelope(text: str, *, strict: bool):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('DUPLICATE_JSON_FIELD')
            out[key] = value
        return out
    try:
        parsed = json.loads(text, object_pairs_hook=unique, strict=strict)
    except (ValueError, TypeError, RecursionError):
        return None
    if (isinstance(parsed, dict) and set(parsed) == {'body', 'commitments'}
            and all(isinstance(v, str) for v in parsed.values())):
        return parsed
    return None


def unwrap_envelope(content: str) -> tuple[dict | None, list[str], bool]:
    """Declared envelope unwrap. Repairs the CARRIER of the reply, never its content.

    Ollama cloud accepts response_format json_object without enforcing it, so a reply may
    arrive inside a code fence or with control characters inside its strings. Exactly two
    repairs are permitted, both recorded per call; the raw bytes are preserved untouched.
    """
    repairs: list[str] = []
    strict_ok = _envelope(content, strict=True) is not None
    parsed = _envelope(content, strict=True)
    text = content
    if parsed is None:
        match = FENCE.match(content)
        if match:
            text = match.group('inner')
            repairs.append('strip_outer_code_fence')
            parsed = _envelope(text, strict=True)
    if parsed is None:
        candidate = _envelope(text, strict=False)
        if candidate is not None:
            repairs.append('json_strict_false')
            parsed = candidate
    return parsed, repairs, strict_ok


def decode_contribution(record: dict, payload: dict, spec: dict) -> dict:
    """Modelled on tools/multicycle_commitment_study.py `decode_contribution`.

    Declared differences from the H005 decoder, both forced by the multi-endpoint set:
      * a provider that reports no usage yields usage_status UNKNOWN, not a failure
        (EXPERIMENT_METHOD: "Missing usage is unknown, not zero");
      * the delivered text passes through `unwrap_envelope` before the two-field envelope
        test, and the repairs applied are recorded per call.
    Native reasoning may be present (most Ollama models emit it by default); only
    *persisted* reasoning text is a custody failure.
    """
    if record.get('request') != payload or record.get('request_sha256') != digest(payload):
        raise ValueError('PROVIDER_REQUEST_CUSTODY')
    content = record.get('content')
    if not isinstance(content, str) or not content.strip():
        raise ValueError('NO_PUBLIC_CONTENT')
    if record.get('reasoning_content_persisted') or record.get('credential_redaction'):
        raise ValueError('PROVIDER_CONTENT_CUSTODY')
    usage, usage_status = record.get('usage'), 'REPORTED'
    if not isinstance(usage, dict) or not usage:
        usage, usage_status = None, 'UNKNOWN'
    else:
        for key in ('prompt_tokens', 'completion_tokens'):
            if type(usage.get(key)) is not int or usage[key] < 0:
                usage, usage_status = None, 'UNKNOWN'
                break
        else:
            if usage['completion_tokens'] > spec['max_tokens']:
                raise ValueError('PROVIDER_CAP_EXCEEDED')
    delivery = DELIVERY.get((record.get('status'), record.get('finish_reason')))
    if delivery is None:
        raise ValueError('PROVIDER_NOT_USABLE')
    envelope, repairs, strict_ok = unwrap_envelope(content)
    body = envelope['body'] if envelope else content
    commitments = envelope['commitments'] if envelope else ''
    return {'body': body, 'commitments': commitments,
            'delivery_status': delivery,
            'envelope_status': 'AUTHORED' if envelope else 'OPAQUE',
            'envelope_repairs': repairs,
            'strict_parse_would_succeed': strict_ok,
            'comparable': delivery != 'PARTIAL',
            # V2: the PARTIAL reason names this coordinate's own declared ceiling.
            'unresolved_reason': (None if delivery != 'PARTIAL'
                                  else partial_unresolved(spec['max_tokens'])),
            'usage': usage, 'usage_status': usage_status,
            'provider_status': record.get('status'),
            'finish_reason': record.get('finish_reason'),
            'returned_model': record.get('returned_model'),
            'reasoning_content_present': bool(record.get('reasoning_content_present')),
            # The OpenAI-compatible families do not echo a seed at the top level of a
            # call record. Reporting `False` there asserted an absence the field could
            # never contradict, so the field is tri-state: the echoed value when the
            # provider actually returned one, otherwise None - unknown, not denied
            # (FW5:634). `system_fingerprint` is the determinism signal these families
            # do return, and it is recorded beside it.
            'seed_echoed_in_response': (record['seed'] if isinstance(record.get('seed'), int)
                                        else None),
            'seed_echo_reported': 'seed' in record,
            'system_fingerprint': (record['system_fingerprint']
                                   if isinstance(record.get('system_fingerprint'), str) else None),
            'public_text_sha256': tsha(content), 'body_sha256': tsha(body),
            'commitments_sha256': tsha(commitments)}


# ------------------------------------------------------------------ dispatch

class KeyGate:
    """At most `MAX_CONCURRENT_PER_KEY` in flight per credential, in this driver.

    The transport holds the same ceiling process-wide; this is the study's own gate so
    the authorisation does not depend on a single implementation.
    """

    def __init__(self, limit: int = MAX_CONCURRENT_PER_KEY) -> None:
        self.limit = limit
        self._lock = threading.Lock()
        self._slots: dict[str, threading.BoundedSemaphore] = {}

    def slot(self, key_env: str) -> threading.BoundedSemaphore:
        with self._lock:
            if key_env not in self._slots:
                self._slots[key_env] = threading.BoundedSemaphore(self.limit)
            return self._slots[key_env]


def build_waves(plan: dict) -> list[dict]:
    """Deterministic waves: no key appears more than `MAX_CONCURRENT_PER_KEY` times in one."""
    key_env = {e['slug']: e['key_env'] for e in plan['endpoints']}
    waves, current, counts = [], [], {}
    for coord in plan['coordinates']:
        key = key_env[coord['endpoint_slug']]
        if counts.get(key, 0) >= MAX_CONCURRENT_PER_KEY:
            waves.append(current)
            current, counts = [], {}
        current.append(coord)
        counts[key] = counts.get(key, 0) + 1
    if current:
        waves.append(current)
    return [{'wave_id': f'wave{index + 1:04d}', 'coordinates': wave}
            for index, wave in enumerate(waves)]


def run(output: Path, plan_id: str, repo: Path, *, provider_factory=None,
        notify: Callable[[str], None] = print,
        only: Callable[[dict], bool] | None = None, resume: bool = False) -> dict:
    """Dispatch by waves, write-once, no replay.

    `resume=True` completes an interrupted occurrence: a coordinate that already has a
    terminal receipt (`responses/<...>.json`) is skipped, and a coordinate that has a
    request or an attempt but NO receipt still raises NO_REPLAY - that is the genuinely
    ambiguous case, where a call may have reached the provider and been billed, and it
    is never silently re-sent.
    """
    material, plan = verify(output, repo)
    if plan['plan_id'] != plan_id:
        raise ValueError('PLAN_ID_MISMATCH')
    output = Path(output)
    endpoints = {e['slug']: e for e in material['endpoints']}
    planned_timeouts = {e['slug']: e['timeout_seconds'] for e in plan['endpoints']}
    factory = provider_factory or live_provider
    gate = KeyGate()
    waves = build_waves(plan)
    results, dispatched, skipped = [], 0, 0

    for wave in waves:
        selected = [c for c in wave['coordinates'] if only is None or only(c)]
        if resume:
            done = [c for c in selected if at(output, 'responses', c).exists()]
            skipped += len(done)
            selected = [c for c in selected if not at(output, 'responses', c).exists()]
        if not selected:
            continue
        for coord in selected:
            for category in ('requests', 'attempts', 'responses'):
                if at(output, category, coord).exists():
                    raise FileExistsError('NO_REPLAY')
        wave_path = output / 'waves' / (wave['wave_id'] + '.json')
        # A wave is defined by the plan (`build_waves`), not by what one invocation chose
        # to dispatch, so the record is the same bytes under any filter and under a
        # resume. That makes the re-verify below meaningful: it fires on a real
        # redefinition of a published wave, never on a legitimate continuation.
        record = {'schema': 'minireason.c001.wave.v1', 'wave_id': wave['wave_id'],
                  'plan_id': plan['plan_id'], 'coordinates': wave['coordinates'],
                  'note': ('the wave as the plan defines it; which of its coordinates were '
                           'dispatched is in requests/ attempts/ responses/')}
        if wave_path.exists():
            # Write-once with an idempotent re-verify, so a resumed run cannot quietly
            # redefine a wave that was already published.
            if load(wave_path) != record:
                raise ValueError('WAVE_CHANGED')
        else:
            write_new(wave_path, record)

        def send(coord: dict, wave_id: str = wave['wave_id']) -> dict:
            endpoint = endpoints[coord['endpoint_slug']]
            spec = spec_for(endpoint, coord)
            messages = messages_for(material, coord['arm'], coord['case'])
            frozen = plan['briefs'][coord['arm']]['cases'][coord['case']]
            if digest(messages) != frozen['messages_sha256']:
                raise ValueError('BRIEF_DIGEST_MISMATCH')
            # The declared wall-clock timeout, re-read off the FROZEN PLAN before the
            # send and written into the request record, so what this coordinate ran
            # under is published rather than inferred from the registry's default.
            if spec['timeout_seconds'] != planned_timeouts.get(coord['endpoint_slug']):
                raise ValueError('TIMEOUT_NOT_APPLIED')
            payload = payload_for(messages, spec)
            request = {'schema': 'minireason.c001.request.v1', 'coordinate': coord,
                       'plan_id': plan['plan_id'], 'wave_id': wave_id,
                       'messages': messages, 'messages_sha256': digest(messages),
                       'provider_payload': payload, 'provider_payload_sha256': digest(payload),
                       'spec': spec, 'timeout_seconds': spec['timeout_seconds'],
                       'brief_sha256': frozen['brief_sha256'],
                       'objection_projection_sha256': frozen['objection_projection_sha256'],
                       'shared_prefix_sha256': plan['briefs'][coord['arm']]['shared_prefix_sha256'],
                       'shared_suffix_sha256': plan['briefs'][coord['arm']]['shared_suffix_sha256'],
                       'varies_only': 'the objection projection block'}
            write_new(at(output, 'requests', coord), request)
            write_new(at(output, 'attempts', coord),
                      {'schema': 'minireason.c001.attempt.v1', 'coordinate': coord,
                       'request_sha256': digest(request), 'wave_id': wave_id,
                       'plan_id': plan['plan_id'], 'started_utc': utc(),
                       'automatic_retry': False})
            receipt = {'schema': 'minireason.c001.receipt.v1', 'coordinate': coord,
                       'request_sha256': digest(request), 'finished_utc': utc(),
                       'status': 'FAILED', 'failure_type': None, 'failure_class': None,
                       'validation_failure_type': None, 'validation_failure_class': None,
                       'envelope_status': None,
                       'envelope_repairs': None, 'strict_parse_would_succeed': None,
                       'comparable': False, 'unresolved_reason': None,
                       'usage': None, 'usage_status': 'UNKNOWN', 'provider_status': None,
                       'returned_model': None, 'finish_reason': None,
                       'reasoning_content_present': None,
                       'honors_seed': spec['honors_seed'],
                       'timeout_seconds': spec['timeout_seconds'],
                       'seed_requested': spec['seed_requested'], 'seed_sent': spec['seed'],
                       'seed_echoed_in_response': None, 'seed_echo_reported': None,
                       'system_fingerprint': None,
                       'provider_request_sha256': None, 'provider_response_sha256': None}
            records = provider_dir(output, coord)
            with gate.slot(spec['key_env']):
                try:
                    factory(endpoint, records).complete(
                        messages, response_format={'type': 'json_object'},
                        max_tokens=spec['max_tokens'], temperature=None, seed=spec['seed'],
                        coordinate={'study': 'C001', **coord})
                except Exception as exc:
                    # ProviderFailure carries a declared code (HTTP_429, KEY_MISSING,
                    # TRANSPORT_OR_RESPONSE_ERROR, CONTENT_TYPE, SECRET_IN_REQUEST).
                    # Recording only the class name made every transport outcome the
                    # string 'ProviderFailure' across a 240-call run.
                    receipt['failure_type'] = failure_code(exc)
                    receipt['failure_class'] = type(exc).__name__
            for name, field in (('call-0001.request.json', 'provider_request_sha256'),
                                ('call-0001.response.json', 'provider_response_sha256')):
                if (records / name).exists():
                    receipt[field] = sha((records / name).read_bytes())
            try:
                record = load(records / 'call-0001.response.json')
                if isinstance(record.get('content'), str):
                    write_new(at(output, 'responses', coord, 'txt'),
                              record['content'].encode('utf-8'))
                contribution = decode_contribution(record, payload, spec)
                write_new(at(output, 'artifacts', coord),
                          {'schema': 'minireason.c001.artifact.v1', 'coordinate': coord,
                           'plan_id': plan['plan_id'], **contribution})
                receipt.update({k: contribution[k] for k in (
                    'delivery_status', 'envelope_status', 'envelope_repairs',
                    'strict_parse_would_succeed', 'comparable', 'unresolved_reason', 'usage',
                    'usage_status', 'provider_status', 'returned_model', 'finish_reason',
                    'reasoning_content_present', 'seed_echoed_in_response',
                    'seed_echo_reported', 'system_fingerprint')})
                receipt['status'] = receipt.pop('delivery_status')
                receipt['artifact_sha256'] = sha(at(output, 'artifacts', coord).read_bytes())
            except Exception as exc:
                receipt['validation_failure_type'] = failure_code(exc)
                receipt['validation_failure_class'] = type(exc).__name__
            write_new(at(output, 'responses', coord), receipt)
            notify(json.dumps({'coordinate': label(coord), 'status': receipt['status'],
                               'envelope_status': receipt['envelope_status'],
                               'envelope_repairs': receipt['envelope_repairs']}))
            return receipt

        with ThreadPoolExecutor(max_workers=len(selected)) as executor:
            for receipt in executor.map(send, selected):
                results.append(receipt)
                dispatched += 1

    return {'plan_id': plan['plan_id'], 'dispatched': dispatched, 'waves': len(waves),
            'resumed': bool(resume), 'skipped_already_terminal': skipped,
            'planned_calls': plan['planned_calls'],
            'statuses': sorted({r['status'] for r in results})}


# ------------------------------------------------------------------ audit

def read_terminal(output: Path, coord: dict, plan: dict | None = None) -> dict:
    request = load(at(output, 'requests', coord))
    attempt = load(at(output, 'attempts', coord))
    receipt = load(at(output, 'responses', coord))
    if any(v.get('coordinate') != coord for v in (request, attempt, receipt)):
        raise ValueError('TERMINAL_CUSTODY_MISMATCH')
    if (attempt['request_sha256'] != digest(request)
            or receipt['request_sha256'] != digest(request)
            or request['messages_sha256'] != digest(request['messages'])
            or request['provider_payload'] != payload_for(request['messages'], request['spec'])
            or request['provider_payload_sha256'] != digest(request['provider_payload'])):
        raise ValueError('TERMINAL_CUSTODY_MISMATCH')
    if plan is not None:
        # The request is re-tied to the FROZEN PLAN, not merely to itself. Without this
        # a record set is internally consistent about a brief that was never planned,
        # and the one claim C001 makes - that only the objection block varied - is not
        # re-derivable from the published records.
        if request.get('plan_id') != plan['plan_id'] or attempt.get('plan_id') != plan['plan_id']:
            raise ValueError('REQUEST_NOT_FROM_PLAN')
        arm_briefs = plan['briefs'][coord['arm']]
        frozen = arm_briefs['cases'][coord['case']]
        if (request['messages_sha256'] != frozen['messages_sha256']
                or request.get('brief_sha256') != frozen['brief_sha256']
                or request.get('objection_projection_sha256')
                != frozen['objection_projection_sha256']
                or request.get('shared_prefix_sha256') != arm_briefs['shared_prefix_sha256']
                or request.get('shared_suffix_sha256') != arm_briefs['shared_suffix_sha256']):
            raise ValueError('REQUEST_NOT_FROM_PLAN')
        if tsha(request['messages'][1]['content']) != frozen['brief_sha256']:
            raise ValueError('REQUEST_NOT_FROM_PLAN')
        # The wall-clock timeout this coordinate ran under, re-tied to the plan. A
        # record that says 180 where the plan froze 600 is a record of a different
        # configuration, whatever else about it is self-consistent.
        planned_timeout = next((e['timeout_seconds'] for e in plan['endpoints']
                                if e['slug'] == coord['endpoint_slug']), None)
        if (request.get('timeout_seconds') != planned_timeout
                or request['spec'].get('timeout_seconds') != planned_timeout
                or receipt.get('timeout_seconds') != planned_timeout):
            raise ValueError('TIMEOUT_NOT_APPLIED')
    records = provider_dir(output, coord)
    for name, field in (('call-0001.request.json', 'provider_request_sha256'),
                        ('call-0001.response.json', 'provider_response_sha256')):
        actual = sha((records / name).read_bytes()) if (records / name).exists() else None
        if actual != receipt.get(field):
            raise ValueError('PROVIDER_BYTES_CHANGED')
    if receipt['status'] in ('COMPLETE', 'PARTIAL'):
        path = at(output, 'artifacts', coord)
        artifact = load(path)
        if (sha(path.read_bytes()) != receipt['artifact_sha256']
                or artifact['delivery_status'] != receipt['status']
                or artifact['envelope_status'] != receipt['envelope_status']
                or artifact['comparable'] != receipt['comparable']
                or at(output, 'responses', coord, 'txt').read_bytes()
                != load(records / 'call-0001.response.json')['content'].encode('utf-8')):
            raise ValueError('ARTIFACT_CUSTODY_MISMATCH')
        # The artifact's own content digests are RE-DERIVED from the delivered bytes,
        # not merely compared with the receipt. Otherwise an artifact whose body no
        # longer corresponds to anything the model returned survives the audit.
        derived = decode_contribution(load(records / 'call-0001.response.json'),
                                      request['provider_payload'], request['spec'])
        for field in ('body', 'commitments', 'body_sha256', 'commitments_sha256',
                      'public_text_sha256', 'envelope_status', 'envelope_repairs',
                      'strict_parse_would_succeed', 'delivery_status', 'comparable',
                      'usage', 'usage_status', 'finish_reason', 'provider_status',
                      'returned_model'):
            if artifact.get(field) != derived[field]:
                raise ValueError('ARTIFACT_NOT_DERIVED_FROM_DELIVERY')
        if (tsha(artifact['body']) != artifact['body_sha256']
                or tsha(artifact['commitments']) != artifact['commitments_sha256']):
            raise ValueError('ARTIFACT_NOT_DERIVED_FROM_DELIVERY')
    elif receipt['status'] != 'FAILED':
        raise ValueError('TERMINAL_STATUS_INVALID')
    return receipt


def audit(output: Path, repo: Path) -> dict:
    material, plan = verify(output, repo)
    output = Path(output)
    counts = {'COMPLETE': 0, 'PARTIAL': 0, 'FAILED': 0, 'AUTHORED': 0, 'OPAQUE': 0,
              'unresolved_partial': 0, 'unresolved_attempts': 0, 'not_dispatched': 0,
              'envelope_repaired': 0}
    usage = {'prompt_tokens': 0, 'completion_tokens': 0}
    failures: dict[str, int] = {}
    unknown_usage, cells, seeds = 0, [], {}
    for coord in plan['coordinates']:
        if at(output, 'responses', coord).exists():
            receipt = read_terminal(output, coord, plan)
            counts[receipt['status']] += 1
            if receipt['envelope_status'] in ('AUTHORED', 'OPAQUE'):
                counts[receipt['envelope_status']] += 1
            if receipt['envelope_repairs']:
                counts['envelope_repaired'] += 1
            if receipt['status'] == 'PARTIAL':
                counts['unresolved_partial'] += 1
            if receipt['usage_status'] == 'REPORTED' and isinstance(receipt['usage'], dict):
                for name in usage:
                    usage[name] += int(receipt['usage'].get(name, 0))
            else:
                unknown_usage += 1
            for field in ('failure_type', 'validation_failure_type'):
                code = receipt.get(field)
                if code:
                    failures[code] = failures.get(code, 0) + 1
            # Aggregated over replicates. Assigning per coordinate made a field named
            # per-endpoint report whatever the last replicate happened to carry.
            entry = seeds.setdefault(coord['endpoint_slug'], {
                'honors_seed': receipt['honors_seed'], 'honors_seed_constant': True,
                'seeds_sent': [], 'seed_echoes_reported': 0, 'seed_echoes': [],
                'system_fingerprints': [], 'coordinates': 0})
            entry['coordinates'] += 1
            if entry['honors_seed'] != receipt['honors_seed']:
                entry['honors_seed_constant'] = False
            if receipt['seed_sent'] not in entry['seeds_sent']:
                entry['seeds_sent'].append(receipt['seed_sent'])
            if receipt.get('seed_echo_reported'):
                entry['seed_echoes_reported'] += 1
            if (receipt.get('seed_echoed_in_response') is not None
                    and receipt['seed_echoed_in_response'] not in entry['seed_echoes']):
                entry['seed_echoes'].append(receipt['seed_echoed_in_response'])
            if (receipt.get('system_fingerprint')
                    and receipt['system_fingerprint'] not in entry['system_fingerprints']):
                entry['system_fingerprints'].append(receipt['system_fingerprint'])
            state = receipt['status']
        elif at(output, 'attempts', coord).exists():
            counts['unresolved_attempts'] += 1
            unknown_usage += 1
            state = 'UNRESOLVED'
        else:
            counts['not_dispatched'] += 1
            state = 'NOT_DISPATCHED'
        cells.append({'coordinate': label(coord), 'state': state})
    for entry in seeds.values():
        entry['seeds_sent'] = sorted(x for x in entry['seeds_sent'] if x is not None)
        entry['seed_echoes'] = sorted(entry['seed_echoes'])
        entry['system_fingerprints'] = sorted(entry['system_fingerprints'])
    return {'plan_id': plan['plan_id'], 'planned_calls': plan['planned_calls'],
            'counts': counts, 'known_usage': usage, 'unknown_usage_calls': unknown_usage,
            'failure_codes': dict(sorted(failures.items())),
            'max_tokens_by_endpoint': {e['id']: e['max_tokens'] for e in plan['endpoints']},
            'timeout_seconds_by_endpoint': {e['id']: e['timeout_seconds']
                                            for e in plan['endpoints']},
            'seed_by_endpoint': seeds, 'cells': cells}


# ------------------------------------------------------------------ comparison

def fcl_structure(text: str) -> dict:
    doc = json.loads(text)
    return {'language': doc.get('language'),
            'record_ids': [r['id'] for r in doc['records']],
            'types': {r['id']: r['type'] for r in doc['records']},
            'fields': {r['id']: sorted(k for k in r if k not in ('id', 'type'))
                       for r in doc['records']},
            'references': {r['id']: {k: list(r[k]) for k in FCL_REF_FIELDS if k in r}
                           for r in doc['records']},
            'uptake': list(doc.get('uptake', []))}


def token_occurrences(text: str, tokens: list[str]) -> dict[str, int]:
    """Genuinely UNQUALIFIED occurrences of each token.

    A match preceded by '#' or '.' belongs to a structured reference ('<address>#o1',
    'o1.text') and is already counted in the prefix-resolved channel; counting it here
    too would make two channels PLAN \u00a77 presents as separate overlap by construction.
    """
    out = {}
    for token in tokens:
        count = len(re.findall(r'(?<![A-Za-z0-9_#.])' + re.escape(token) + r'(?![A-Za-z0-9_])',
                               text))
        if count:
            out[token] = count
    return out


def resolve_ref(value: str, addresses: dict) -> tuple[str | None, str, str]:
    """Split one reference into (document, record_id, how the prefix was resolved).

    A cross-document reference is '<prefix>#<record id>'. The prefix identifies WHICH
    document is referenced, and the objection and the account share five of the
    objection's eight record ids, so dropping it attributes five of eight to the
    objection whichever document was actually cited. The prefix is matched against each
    declared artifact address, that address truncated to its first 16 hex characters
    (the form the real H005 response node emitted), and the source name itself. An
    unrecognised prefix resolves to no document; a reference with no prefix at all is
    not a cross-document reference and stays in the bare-token channel.
    """
    text = str(value)
    if '#' not in text:
        return None, text, 'BARE'
    prefix, record_id = text.split('#', 1)
    cut = int(addresses.get('truncation_chars') or 16)
    for name in ('objection', 'account', 'rival'):
        address = str(addresses.get(name) or '')
        if not address:
            continue
        if prefix == address:
            return name, record_id, 'FULL_ADDRESS'
        if len(address) >= cut and prefix == address[:cut]:
            return name, record_id, 'TRUNCATED_ADDRESS'
        if prefix == name:
            return name, record_id, 'SOURCE_NAME'
    return None, record_id, 'UNRECOGNISED_PREFIX'


def fcl_surface(commitments: str, objection_ids: list[str], addresses: dict) -> dict:
    empty = {'record_count': None, 'record_ids': None, 'records_by_type': None,
             'records_of_undeclared_type': None, 'targets_named': None,
             'reference_fields': None, 'cross_document_refs': None,
             'refs_by_document': None, 'ref_prefix_forms': None,
             'objection_record_ids_in_refs': None, 'account_prefixed_refs': None,
             'rival_prefixed_refs': None, 'unresolved_prefix_refs': None,
             'bare_refs_unresolved': None, 'uptake': None, 'language': None}
    try:
        doc = json.loads(commitments)
    except (ValueError, TypeError):
        return {'parse': 'FAILED', **empty}
    if not isinstance(doc, dict) or not isinstance(doc.get('records'), list):
        return {'parse': 'NOT_FCL', **empty}
    records = [r for r in doc['records'] if isinstance(r, dict)]
    references = {field: sorted({str(v) for r in records for v in (r.get(field) or [])})
                  for field in FCL_REF_FIELDS}
    values = sorted({str(v) for field in FCL_REF_FIELDS
                     for r in records for v in (r.get(field) or [])})
    by_document: dict[str, list[str]] = {'objection': [], 'account': [], 'rival': []}
    forms: dict[str, int] = {}
    unresolved_prefix, bare = [], []
    for value in values:
        document, record_id, form = resolve_ref(value, addresses)
        forms[form] = forms.get(form, 0) + 1
        if form == 'BARE':
            bare.append(value)
        elif document is None:
            unresolved_prefix.append(value)
        elif record_id not in by_document[document]:
            by_document[document].append(record_id)
    for name in by_document:
        by_document[name] = sorted(by_document[name])
    ids = set(objection_ids or ())
    return {'parse': 'OK', 'language': doc.get('language'), 'record_count': len(records),
            'record_ids': [str(r.get('id')) for r in records],
            'records_by_type': {t: sum(1 for r in records if r.get('type') == t) for t in FCL_TYPES},
            'records_of_undeclared_type': sorted(
                {str(r.get('type')) for r in records if r.get('type') not in FCL_TYPES}),
            'targets_named': references['target'], 'reference_fields': references,
            'cross_document_refs': [v for v in values if '#' in v],
            'refs_by_document': by_document, 'ref_prefix_forms': dict(sorted(forms.items())),
            'objection_record_ids_in_refs': sorted(set(by_document['objection']) & ids)
            if ids else sorted(by_document['objection']),
            'account_prefixed_refs': sorted(by_document['account']),
            'rival_prefixed_refs': sorted(by_document['rival']),
            'unresolved_prefix_refs': sorted(unresolved_prefix),
            'bare_refs_unresolved': sorted(v for v in bare if v in ids),
            'uptake': ([str(v) for v in doc['uptake']]
                       if isinstance(doc.get('uptake'), list) else None)}


def surface_for(artifact: dict, arm: str, objection_ids: list[str],
                addresses: dict | None = None) -> dict:
    common = {'delivery_status': artifact['delivery_status'],
              'envelope_status': artifact['envelope_status'],
              'envelope_repairs': artifact['envelope_repairs'],
              'strict_parse_would_succeed': artifact['strict_parse_would_succeed'],
              'comparable': artifact['comparable'],
              'unresolved_reason': artifact['unresolved_reason'],
              'public_text_sha256': artifact['public_text_sha256'],
              'body_sha256': artifact['body_sha256'],
              'commitments_sha256': artifact['commitments_sha256'],
              'body_chars': len(artifact['body']),
              'commitments_chars': len(artifact['commitments'])}
    if not artifact['comparable']:
        # A truncated surface is not compared against another case (FW5:634).
        common['mechanical'] = 'withheld: cell unresolved'
        return common
    if arm == 'prose':
        # For a prose commitment surface this study claims nothing mechanical beyond
        # byte identity and length; root reads the text (FW5:630, a semantic comparison).
        common['mechanical'] = 'none beyond byte hashes and lengths'
        return common
    common['fcl'] = fcl_surface(artifact['commitments'], objection_ids, addresses or {})
    common['objection_id_tokens_in_body'] = token_occurrences(artifact['body'], objection_ids or [])
    common['objection_id_tokens_in_commitments'] = token_occurrences(
        artifact['commitments'], objection_ids or [])
    common['token_ambiguity'] = ('bare record-id tokens are shared with the account document; '
                                 'which document a bare token names is not mechanically '
                                 'resolvable and stays unresolved (FW5:634). A token preceded '
                                 "by '#' or '.' belongs to a structured reference and is counted "
                                 'only in the prefix-resolved channel, never here.')
    return common


EMPTY_ROOT_COLUMNS = ('original_vs_control', 'original_vs_recoding', 'original_vs_carrier',
                      'pattern_read', 'grounds', 'unresolved')


def comparison(output: Path, repo: Path) -> dict:
    material, plan = verify(output, repo)
    output = Path(output)
    cells: dict[tuple[str, str], dict] = {}
    for coord in plan['coordinates']:
        key = (coord['endpoint_slug'], coord['arm'])
        block = material['arms'][coord['arm']]
        ids = block['objection_source']['record_ids'] or []
        addresses = block['artifact_addresses']
        entry = cells.setdefault(key, {case: [] for case in CASES})
        path = at(output, 'artifacts', coord)
        # The delivered bytes are on disk whenever any text reached us, including for a
        # delivery the decoder refused. Root most needs to read exactly those replies,
        # so the path is set from the .txt, independently of whether an artifact exists.
        text_path = at(output, 'responses', coord, 'txt')
        delivered = text_path.relative_to(output).as_posix() if text_path.exists() else None
        if path.exists():
            entry[coord['case']].append(
                {'replicate': coord['replicate'], 'state': 'PRESENT', 'path': delivered,
                 **surface_for(load(path), coord['arm'], ids, addresses)})
        elif at(output, 'responses', coord).exists():
            receipt = load(at(output, 'responses', coord))
            entry[coord['case']].append(
                {'replicate': coord['replicate'], 'path': delivered, 'state': 'FAILED',
                 'failure_type': receipt.get('failure_type'),
                 'validation_failure_type': receipt.get('validation_failure_type'),
                 'provider_status': receipt.get('provider_status'),
                 'finish_reason': receipt.get('finish_reason'),
                 'delivered_text_present': delivered is not None,
                 'comparable': False,
                 'unresolved_reason': ('delivery refused; the delivered bytes are printed in the '
                                       'juxtaposition and the cell stays unresolved (FW5:634)')})
        else:
            entry[coord['case']].append(
                {'replicate': coord['replicate'], 'path': None, 'state': 'NOT_DISPATCHED'})
    out = {'schema': 'minireason.c001.comparison.v1', 'plan_id': plan['plan_id'],
           'question': plan['question'], 'claim_ceiling': plan['claim_ceiling'],
           'partial_delivery_rule': plan['partial_delivery_rule'],
           'reading_rule': plan['reading_rule'],
           'reading_note': ('"differs against control, not under recoding, not under carrier '
                            'disturbance" is a pattern root reads off these surfaces. It is never '
                            'computed here and never expressed as a quantity (FW5:628, :630, :851).'),
           'tables': []}
    for (endpoint_slug, arm), entry in sorted(cells.items()):
        unresolved = [f'{case}/rep{row["replicate"]}' for case in CASES for row in entry[case]
                      if row['state'] != 'PRESENT' or not row.get('comparable', False)]
        out['tables'].append({'endpoint_slug': endpoint_slug, 'arm': arm, 'cases': entry,
                              'unresolved_cells': unresolved,
                              'root_reading': {column: '' for column in EMPTY_ROOT_COLUMNS},
                              'root_register_marks': {
                                  row: {register['id']: '' for register in
                                        plan['reading_rule']['registers']}
                                  for row in REGISTER_MARK_ROWS}})
    assert_no_scoring_keys(out)
    return out


def _cell(value: Any) -> str:
    """One rendered scalar, safe inside a markdown table cell.

    Three of the values that reach here - record ids, targets named, uptake - are read
    straight out of the successor's own document, so a '|' or a newline in model output
    would otherwise corrupt the table for that endpoint.
    """
    return str(value).replace('\\', '\\\\').replace('|', '\\|').replace(
        '\r', ' ').replace('\n', ' ')


def _md(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, (list, tuple)):
        return ', '.join(_cell(v) for v in value) if value else '(none)'
    if isinstance(value, dict):
        return (', '.join(f'{_cell(k)}={_cell(v)}' for k, v in sorted(value.items()))
                if value else '(none)')
    return _cell(value)


FCL_HEAD = ('case', 'rep', 'delivery', 'envelope', 'repairs', 'strict parse', 'comparable',
            'fcl parse', 'records', 'by type', 'record ids', 'targets named',
            'objection ids in refs (prefix-resolved)', 'account-prefixed refs',
            'rival-prefixed refs', 'refs with an unrecognised prefix',
            'bare id refs (unresolved)', 'uptake', 'body sha256', 'commitments sha256',
            'body chars', 'commitments chars')
PROSE_HEAD = ('case', 'rep', 'delivery', 'envelope', 'repairs', 'strict parse', 'comparable',
              'body sha256', 'commitments sha256', 'body chars', 'commitments chars')
REGISTER_MARK_ROWS = ('within ORIGINAL (baseline, written first)', 'ORIGINAL vs CONTROL',
                      'ORIGINAL vs RECODING', 'ORIGINAL vs CARRIER')


def render_comparison(data: dict) -> str:
    rule = data['reading_rule']
    lines = ['# C001 comparison: successor commitment surfaces across four cases', '',
             f'plan_id: `{data["plan_id"]}`', '',
             '**Question.** ' + data['question'], '',
             '**Claim ceiling.** ' + data['claim_ceiling'], '',
             '**Unresolved cells.** ' + data['partial_delivery_rule'], '',
             '**How to read this.** ' + data['reading_note'], '',
             "Every `root_*` cell below is deliberately empty. Root fills it by reading the raw "
             'juxtaposition; nothing in this file computes it.', '',
             '## What "differs" means, pre-declared', '',
             rule['preamble'], '',
             '| register | reads | `differs` iff |', '|---|---|---|']
    lines += ['| `{}` {} | {} | {} |'.format(_cell(r['id']), _cell(r['name']), _cell(r['reads']),
                                             _cell(r['differs_iff'])) for r in rule['registers']]
    lines += ['', '**The replicate baseline.** ' + rule['replicate_baseline'], '',
              '**Order of reading.** ' + rule['order_of_reading'], '',
              '**Two readers.** ' + rule['two_readers'], '',
              '**Never aggregated.** ' + rule['never_aggregated'], '']
    for table in data['tables']:
        arm = table['arm']
        head = FCL_HEAD if arm == 'fcl' else PROSE_HEAD
        lines += [f'## {table["endpoint_slug"]} / {arm}', '',
                  '| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|']
        for case in CASES:
            for row in table['cases'][case]:
                if row['state'] != 'PRESENT':
                    refusal = _md(row.get('validation_failure_type')
                                  or row.get('failure_type') or '')
                    state = row['state'] + (f' ({refusal})' if refusal else '')
                    lines.append('| ' + ' | '.join([case, str(row['replicate']), state]
                                                   + [''] * (len(head) - 3)) + ' |')
                    continue
                prefix = [case, str(row['replicate']), row['delivery_status'],
                          row['envelope_status'], _md(row['envelope_repairs']),
                          _md(row['strict_parse_would_succeed']), _md(row['comparable'])]
                tail = [row['body_sha256'][:16], row['commitments_sha256'][:16],
                        str(row['body_chars']), str(row['commitments_chars'])]
                if arm == 'fcl':
                    fcl = row.get('fcl')
                    middle = ([_md(fcl['parse']), _md(fcl['record_count']),
                               _md(fcl['records_by_type']), _md(fcl['record_ids']),
                               _md(fcl['targets_named']), _md(fcl['objection_record_ids_in_refs']),
                               _md(fcl['account_prefixed_refs']), _md(fcl['rival_prefixed_refs']),
                               _md(fcl['unresolved_prefix_refs']),
                               _md(fcl['bare_refs_unresolved']),
                               _md(fcl['uptake'])] if fcl else ['unresolved'] + [''] * 10)
                    lines.append('| ' + ' | '.join(prefix + middle + tail) + ' |')
                else:
                    lines.append('| ' + ' | '.join(prefix + tail) + ' |')
        lines += ['', '**Unresolved in this cell:** ' + (_md(table['unresolved_cells']) or '(none)'),
                  '', "### Root's reading (empty until root reads the juxtaposition)", '',
                  '| ' + ' | '.join(EMPTY_ROOT_COLUMNS) + ' |',
                  '|' + '|'.join(['---'] * len(EMPTY_ROOT_COLUMNS)) + '|',
                  '| ' + ' | '.join('' for _ in EMPTY_ROOT_COLUMNS) + ' |', '',
                  '### Register marks (empty; one of `differs` / `same` / `unresolved` each)', '',
                  '| comparison | T target named | E objection record engaged | '
                  'D proposed action | G grounds cited |', '|---|---|---|---|---|']
        lines += ['| ' + row + ' |  |  |  |  |' for row in REGISTER_MARK_ROWS]
        lines += ['', '### Raw juxtaposition', '',
                  f'`juxtaposition/{table["endpoint_slug"]}__{arm}.md`', '']
    return '\n'.join(lines) + '\n'


def render_juxtaposition(output: Path, table: dict) -> str:
    lines = [f'# Raw juxtaposition: {table["endpoint_slug"]} / {table["arm"]}', '',
             'Four cases, five replicates, one node. Only the objection projection block differed '
             'between cases. Raw delivered bytes; no comparison is computed here.', '']
    for case in CASES:
        lines += [f'## case: {case}', '']
        for row in table['cases'][case]:
            state = row['state'] if row['state'] != 'PRESENT' else (
                row['delivery_status'] + ('' if row['comparable'] else ', UNRESOLVED'))
            lines += [f'### rep{row["replicate"]} ({state})', '']
            if row['state'] == 'FAILED':
                refusal = (row.get('validation_failure_type') or row.get('failure_type')
                           or 'refusal not recorded')
                lines += [f'Delivery was NOT accepted: `{refusal}`'
                          + (f' (provider status `{row["provider_status"]}`,'
                             f' finish_reason `{row["finish_reason"]}`)'
                             if row.get('provider_status') else '')
                          + '. The cell is unresolved and is not compared against another case '
                            '(FW5:634). The bytes below are what the provider actually delivered.',
                          '']
            if not row.get('path'):
                lines += ['(no delivered text reached disk)', '']
                continue
            text = (Path(output) / row['path']).read_text(encoding='utf-8')
            lines += ['```', text.replace('```', '`\u200b``'), '```', '']
    return '\n'.join(lines) + '\n'


def table(output: Path, repo: Path, *, force: bool = False) -> dict:
    """Render the comparison, the twelve juxtapositions and root's empty columns.

    `comparison.json`, `COMPARISON.md` and `juxtaposition/` are write-once names in a
    write-once occurrence, so a premature render consumes them for good. Unless `force`
    is given, an occurrence with an undispatched coordinate is refused
    (`OCCURRENCE_INCOMPLETE`) rather than rendered into twelve tables of
    NOT_DISPATCHED rows.
    """
    if not force:
        report = audit(output, repo)
        pending = report['counts']['not_dispatched'] + report['counts']['unresolved_attempts']
        if pending:
            raise ValueError('OCCURRENCE_INCOMPLETE')
    data = comparison(output, repo)
    output = Path(output)
    write_new(output / 'comparison.json', data)
    write_new(output / 'COMPARISON.md', render_comparison(data).encode('utf-8'))
    for entry in data['tables']:
        write_new(output / 'juxtaposition' / f'{entry["endpoint_slug"]}__{entry["arm"]}.md',
                  render_juxtaposition(output, entry).encode('utf-8'))
    return {'plan_id': data['plan_id'], 'tables': len(data['tables']),
            'written': ['comparison.json', 'COMPARISON.md',
                        f'juxtaposition/ ({len(data["tables"])} files)']}


def render_recoding_table(material: dict) -> str:
    lines = ['# C001 recoding correspondence table', '',
             'Published before dispatch. Every unit of each original objection document is listed '
             'with its recoded counterpart and the declared rules applied. No model call produced '
             'any entry; the recoding was authored offline by the study designer.', '']
    for arm in ARMS:
        block = material['arms'][arm]
        recoding = block['recoding']
        lines += [f'## arm: {arm} (source {block["source_arm"]})', '',
                  '**Unit definition.** ' + recoding['unit_definition'], '',
                  '**Reconstruction.** ' + recoding['reconstruction'], '', '**Rules.**', '']
        lines += [f'- `{name}` {text}' for name, text in sorted(recoding['rule'].items())]
        lines += ['', '**Declared hedge/modal marker families** (counted per unit by `prepare`; '
                  'a change in any count is `RECODING_HEDGE_FORCE_CHANGED`).', '',
                  '| family | tokens |', '|---|---|']
        lines += ['| `{}` | {} |'.format(m['family'], ', '.join('`%s`' % t for t in m['tokens']))
                  for m in recoding['hedge_markers']]
        lines += ['', recoding['hedge_marker_note'], '']
        if recoding.get('hedge_marker_limits'):
            lines += ['', recoding['hedge_marker_limits'], '']
        lines += ['', '**Invariants.**', ''] + [f'- {i}' for i in recoding['invariants']]
        lines += ['', '**Not exercised.**', ''] + [f'- {i}' for i in recoding['not_exercised']]
        lines += ['', f'**Units: {recoding["unit_count"]}.**', '',
                  '| unit | location | rules | original | recoded |', '|---|---|---|---|---|']
        for unit in recoding['units']:
            lines.append('| `{}` | {} | {} | {} | {} |'.format(
                unit['unit_id'], unit['location'], ' '.join(unit['rules']),
                unit['original'].replace('|', '\\|').replace('\n', ' '),
                unit['recoded'].replace('|', '\\|').replace('\n', ' ')))
        lines += ['', '**Carrier variant (same content, disturbed carrier).**', '']
        lines += [f'- {i}' for i in block['carrier']['operations']]
        lines += ['', '**Grain declaration.** ' + block['carrier']['grain_declaration'], '',
                  '**Normalisation proof.**', '', '| quantity | value |', '|---|---|']
        lines += [f'| {n} | `{v}` |' for n, v in sorted(block['carrier']['proof'].items())]
        lines.append('')
    return '\n'.join(lines) + '\n'


# ------------------------------------------------------------------ cli

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('prepare', 'verify', 'run', 'audit', 'table'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--material', type=Path)
    parser.add_argument('--repo', type=Path,
                        default=Path(os.environ.get('MINIREASON_REPO', '/home/user/miniReason')))
    parser.add_argument('--plan-id')
    parser.add_argument('--force', action='store_true',
                        help='table only: render even though the occurrence has undispatched '
                             'coordinates. The three output names are write-once, so a '
                             'premature render consumes them')
    parser.add_argument('--resume', action='store_true',
                        help='complete an interrupted occurrence: skip coordinates that already '
                             'have a receipt; still refuse a coordinate with a request or attempt '
                             'and no receipt (NO_REPLAY)')
    args = parser.parse_args(argv)
    try:
        if args.operation == 'prepare':
            if args.material is None:
                raise ValueError('MATERIAL_ARGUMENT_REQUIRED')
            result = prepare(args.material, args.output, args.repo)
        elif args.operation == 'verify':
            _, plan = verify(args.output, args.repo)
            result = {'plan_id': plan['plan_id'], 'verified': True}
        elif args.operation == 'run':
            if not args.plan_id:
                raise ValueError('PLAN_ID_REQUIRED')
            result = run(args.output, args.plan_id, args.repo, resume=args.resume)
        elif args.operation == 'audit':
            result = audit(args.output, args.repo)
        else:
            result = table(args.output, args.repo, force=args.force)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        code = str(exc)
        print(json.dumps({'error': code if re.fullmatch('[A-Z0-9_]+', code) else type(exc).__name__}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
