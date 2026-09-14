"""Build experiments/diagnostics/C001-contrast-triple/material.json.

Provenance script. Run offline, before any dispatch. It reads the frozen H005
occurrence (read-only), applies the hand-authored recoding in recoding_units.py
and the declared carrier operations, and writes the frozen four-case material.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recoding_units as RU  # noqa: E402

REPO = Path(os.environ.get('MINIREASON_REPO', '/home/user/miniReason'))
H005 = REPO / 'experiments/diagnostics/H005-open-prose-commitments'
OCC = H005 / 'occurrence-01'
# Published under the study directory as `build/`, so the study directory is this
# file's parent's parent and the driver is the repository's own published `tools/`
# copy. (While staged this script sat at `scratchpad/contrast/.build/` and resolved
# the same two paths relative to that scratchpad root.)
STUDY = Path(__file__).resolve().parents[1]
OUT = STUDY / 'material.json'
TABLE = STUDY / 'RECODING_TABLE.md'
DRIVER_DIR = REPO / 'tools'

SENTENCE = re.compile(r'(?<=[.!?])\s+')
BULLET = re.compile(r'^[ \t]*[-*•]\s+')
ARMS = {'fcl': 'mini_fcl', 'prose': 'mini_prose'}
FIELD_ORDER = ('text', 'scope', 'grounds', 'bearing', 'action', 'consequence')

# Declared before the recoding was re-read. `prepare` counts each family in the
# original and in the recoded text of every unit and refuses a unit whose count
# changed. Contractions are expanded first, so "I'd"/"I would" and "can't"/"cannot"
# count alike.
HEDGE_MARKERS = [
    {'family': 'IF', 'tokens': ['if']},
    {'family': 'UNLESS', 'tokens': ['unless']},
    {'family': 'WHETHER', 'tokens': ['whether']},
    {'family': 'MAY', 'tokens': ['may']},
    {'family': 'MIGHT', 'tokens': ['might']},
    {'family': 'CAN', 'tokens': ['can']},
    {'family': 'COULD', 'tokens': ['could']},
    {'family': 'WILL', 'tokens': ['will']},
    {'family': 'WOULD', 'tokens': ['would']},
    {'family': 'SHALL', 'tokens': ['shall']},
    {'family': 'SHOULD', 'tokens': ['should']},
    {'family': 'MUST', 'tokens': ['must']},
    {'family': 'OUGHT', 'tokens': ['ought']},
    {'family': 'NEED', 'tokens': ['need', 'needs']},
    {'family': 'DESERVE', 'tokens': ['deserve', 'deserves', 'deserved']},
    {'family': 'NECESSARILY', 'tokens': ['necessarily']},
    {'family': 'PROBABLY', 'tokens': ['probably']},
    {'family': 'POSSIBLY', 'tokens': ['possible', 'possibly']},
    {'family': 'PERHAPS', 'tokens': ['perhaps']},
    {'family': 'MERELY', 'tokens': ['merely', 'just', 'simply', 'only']},
    {'family': 'SEEM', 'tokens': ['seem', 'seems']},
    {'family': 'APPEAR', 'tokens': ['appear', 'appears']},
    {'family': 'NEGATION',
     'tokens': ['not', 'never', 'no', 'nor', 'neither', 'none', 'nothing', 'nobody']},
]


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def tsha(text: str) -> str:
    return sha(text.encode('utf-8'))


def split_units(paragraph: str) -> list[str]:
    return SENTENCE.split(paragraph.strip())


def prose_units(text: str) -> list[tuple[str, str]]:
    out = []
    for i, para in enumerate(text.split('\n\n')):
        for j, sentence in enumerate(split_units(para)):
            out.append((f'P{i + 1}.S{j + 1}', sentence))
    return out


def join_prose(units: list[str], shape: list[int]) -> str:
    paragraphs, index = [], 0
    for count in shape:
        paragraphs.append(' '.join(units[index:index + count]))
        index += count
    return '\n\n'.join(paragraphs)


def normalise_prose(text: str) -> str:
    """Declared content-token normalisation for prose carriers."""
    lines = [BULLET.sub('', line) for line in text.splitlines()]
    return ' '.join(' '.join(lines).split())


def canonical_fcl(text: str) -> str:
    """Declared content normalisation for an FCL-1 document.

    Grain declaration: the document's content is the SET of records keyed by id,
    each record being its field->value map, together with the SET of uptake ids
    and the language tag. Array order and key order are carrier.
    """
    doc = json.loads(text)
    out = dict(doc)
    out['records'] = sorted(doc['records'], key=lambda r: r['id'])
    if 'uptake' in doc:
        out['uptake'] = sorted(doc['uptake'])
    return json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def wrap(text: str, width: int = 72) -> str:
    return '\n\n'.join(
        textwrap.fill(p, width=width, break_long_words=False, break_on_hyphens=False)
        for p in text.split('\n\n'))


def bulletise(text: str, width: int = 68) -> str:
    return '\n'.join(
        textwrap.fill(p, width=width, initial_indent='- ', subsequent_indent='  ',
                      break_long_words=False, break_on_hyphens=False)
        for p in text.split('\n\n'))


# ---------------------------------------------------------------- projections

def label(coord: dict) -> str:
    return f'{coord["problem"]}/{coord["arm"]}/cycle-{coord["cycle"]}/{coord["node"]}'


def projection(source: str, view: str, *, coordinate_label: str, artifact_id: str,
               body: str, commitments: str, delivery: str, envelope: str) -> str:
    """Byte-identical to tools/multicycle_commitment_study.py `project` for a present source."""
    lines = [f'Source {source}: {coordinate_label}; selected view: {view}',
             'Artifact: ' + artifact_id,
             'Original body SHA256: ' + tsha(body),
             'Original commitments SHA256: ' + tsha(commitments),
             'Delivery: ' + delivery + '; envelope: ' + envelope]
    if view in ('body', 'both'):
        lines.extend(['BODY', body])
    if view in ('commitments', 'both'):
        lines.extend(['COMMITMENTS', commitments])
    return '\n'.join(lines)


def absent_projection(source: str, view: str) -> str:
    """Byte-identical to `project`'s own absent wording."""
    return ('Source ' + source + ': absent in the first template invocation; selected view '
            + view + '.')


# ---------------------------------------------------------------- recoding

def recode_prose_document(original: str, table: list[tuple[str, list[str], str]],
                          prefix: str) -> tuple[str, list[dict]]:
    units = prose_units(original)
    if len(units) != len(table):
        raise SystemExit(f'UNIT_COUNT_MISMATCH {prefix}: {len(units)} vs {len(table)}')
    shape = [len(split_units(p)) for p in original.split('\n\n')]
    rows = []
    for (uid, text), (tid, rules, recoded) in zip(units, table):
        if prefix + '.' + uid != tid:
            raise SystemExit(f'UNIT_ID_MISMATCH {prefix}.{uid} vs {tid}')
        rows.append({'unit_id': tid, 'location': prefix, 'original': text,
                     'recoded': recoded, 'rules': rules})
    recoded_doc = join_prose([r['recoded'] for r in rows], shape)
    if join_prose([r['original'] for r in rows], shape) != original:
        raise SystemExit(f'ORIGINAL_NOT_RECONSTRUCTIBLE {prefix}')
    return recoded_doc, rows


def recode_fcl_commitments(original: str, table: list[tuple[str, list[str], str]]):
    doc = json.loads(original)
    lookup = {tid: (rules, text) for tid, rules, text in table}
    rows, used = [], set()
    records = []
    for record in doc['records']:
        new = dict(record)
        for field in FIELD_ORDER:
            if field not in record:
                continue
            sentences = split_units(record[field])
            if ' '.join(sentences) != record[field]:
                raise SystemExit(f'FIELD_NOT_RECONSTRUCTIBLE {record["id"]}.{field}')
            recoded = []
            for j, sentence in enumerate(sentences):
                tid = f'K.{record["id"]}.{field}.S{j + 1}'
                if tid not in lookup:
                    raise SystemExit(f'UNIT_UNMAPPED {tid}')
                rules, text = lookup[tid]
                used.add(tid)
                rows.append({'unit_id': tid, 'location': f'commitments/{record["id"]}/{field}',
                             'original': sentence, 'recoded': text, 'rules': rules})
                recoded.append(text)
            new[field] = ' '.join(recoded)
        records.append(new)
    missing = set(lookup) - used
    if missing:
        raise SystemExit(f'UNIT_UNUSED {sorted(missing)}')
    out = dict(doc)
    out['records'] = records
    recoded_doc = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    if json.dumps(doc, ensure_ascii=False, separators=(',', ':')) != original:
        raise SystemExit('FCL_ORIGINAL_NOT_RECONSTRUCTIBLE')
    return recoded_doc, rows


def fcl_structure(text: str) -> dict:
    doc = json.loads(text)
    return {'language': doc.get('language'),
            'record_ids': [r['id'] for r in doc['records']],
            'types': {r['id']: r['type'] for r in doc['records']},
            'fields': {r['id']: sorted(k for k in r if k not in ('id', 'type'))
                       for r in doc['records']},
            'references': {r['id']: {k: list(r[k]) for k in
                                     ('target', 'depends', 'mentions', 'revises', 'withdraws')
                                     if k in r} for r in doc['records']},
            'uptake': list(doc.get('uptake', []))}


# ---------------------------------------------------------------- carriers

def carrier_fcl_commitments(original: str) -> str:
    doc = json.loads(original)
    out = dict(doc)
    out['records'] = list(reversed(doc['records']))
    if 'uptake' in doc:
        out['uptake'] = list(reversed(doc['uptake']))
    return json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)


# ------------------------------------------------------------ reading rule

READING_RULE = {
    'schema': 'minireason.c001.reading_rule.v1',
    'title': 'What "differs" means, pre-declared (PLAN.md \u00a78a)',
    'preamble': (
        'Root reads every cross-case comparison on exactly the four registers below and records for '
        'each one of `differs` / `same` / `unresolved`. The four marks are reported separately and '
        'stand or fall separately; they are never summed, averaged, weighted or reduced to one mark.'),
    'marks': ['differs', 'same', 'unresolved'],
    'registers': [
        {'id': 'T', 'name': 'target named',
         'reads': ("The represented target of the successor's own engagement. FCL arm: the set of values "
                   'in `target` arrays, read with the source artifact prefix intact (a reference into the '
                   'account is not a reference into the objection). Prose arm: the phrase by which the '
                   'successor says what it is responding to.'),
         'differs_iff': 'the two sets of distinct targets are not the same set'},
        {'id': 'E', 'name': 'objection record engaged, prefix-resolved',
         'reads': ("Which of the objection document's records (o1 o2 o3 c1 c2 o4 p1 u1) the successor "
                   "takes up, by prefix-qualified reference or by quotation of that record's own text. "
                   'The prefix is resolved against the declared artifact addresses '
                   '(arms.<arm>.artifact_addresses).'),
         'differs_iff': ('the sets of prefix-resolved objection records engaged are not the same set. A '
                         'bare id token shared with the account document (o1 c1 c2 p1 u1) is `unresolved` '
                         'for this register and never `differs`.')},
        {'id': 'D', 'name': 'proposed action (disposition)',
         'reads': ('What the successor proposes to do about the criticism: use, leave open, revise, reject '
                   'or withdraw. FCL arm: read off record `type`, `uptake`, `revises`, `withdraws` and the '
                   '`action` field. Prose arm: read off the text.'),
         'differs_iff': 'the disposition attached to the same criticism changes'},
        {'id': 'G', 'name': 'grounds cited',
         'reads': ("Whether the successor grounds that disposition in the objection's grounds, the "
                   "account's, the rival's, or none."),
         'differs_iff': 'the cited source of grounds is not the same'},
    ],
    'replicate_baseline': (
        'A register is marked `differs` for a case pair only if the difference root reads between the two '
        'cases is one root does NOT also read between at least one pair of replicates inside ORIGINAL. '
        "Where the same kind of difference already appears inside ORIGINAL's own five replicates, the "
        'register is `same` for that pair and the fact is recorded.'),
    'order_of_reading': (
        'Root reads the five ORIGINAL replicates and writes the within-ORIGINAL spread on all four '
        'registers into COMPARISON.md BEFORE opening any other case\u2019s juxtaposition for that cell. '
        'The baseline note is written first and is not revised afterwards.'),
    'register_to_falsifier': {
        'D1': ('exhibited in a cell only if T, E or D differs ORIGINAL vs CONTROL. G alone does not carry '
               'D1: the control has no objection grounds to cite, so a G difference there is forced by the '
               'design.'),
        'F2': 'fires if T, E or D differs ORIGINAL vs RECODING.',
        'F3': 'fires if T, E or D differs ORIGINAL vs CARRIER.',
    },
    'two_readers': (
        'The registers are written so that two readers of the same juxtaposition mark the same cells. '
        'Where two readers disagree on a register, that register is `unresolved` for that cell and the '
        'disagreement is recorded, never averaged (FW5:634).'),
    'never_aggregated': (
        'No mark is a quantity. The four registers are never summed, averaged, weighted, ranked or '
        'reduced to a single mark (FW5:851; PURPOSE.md, "no scalar progress meter").'),
}


# ------------------------------------------------------------ transport pins

def transport_pins() -> dict:
    """sha256 of the transport module and of the endpoint registry it supplies.

    Both are resolved from the module actually imported, whichever tree that is:
    the staged provider package before publication, the repository's own
    `src/minireason/` after it. `prepare`, `verify`, `run`, `audit` and `table`
    re-hash both on every invocation (TRANSPORT_PIN_MISMATCH).
    """
    import importlib
    extra = os.environ.get('MINIREASON_PROVIDER_SRC')
    if extra and extra not in sys.path:
        sys.path.insert(0, extra)
    module = importlib.import_module('minireason.provider_openai_compat')
    module_path = Path(module.__file__).resolve()
    registry_path = module_path.parent / 'data' / 'endpoints.json'
    return {
        'package': ('minireason, resolved from the imported module: the staged provider '
                    'package before publication, the repository src/minireason/ after it'),
        'module': 'minireason/provider_openai_compat.py',
        'module_sha256': sha(module_path.read_bytes()),
        'registry': 'minireason/data/endpoints.json',
        'registry_sha256': sha(registry_path.read_bytes()),
        'note': ('base_url, chat_path, timeout_seconds and max_concurrency reach this study from '
                 'the transport module and its endpoint registry rather than from this material, '
                 'which is why both are pinned here by sha256 and re-hashed by every command. The '
                 'pinned bytes are the PUBLISHED repository files src/minireason/'
                 'provider_openai_compat.py and src/minireason/data/endpoints.json; an earlier '
                 'build of this material was made while those files existed only in a staging '
                 'provider package, and its note said so, which is no longer true of either file. '
                 'C001 reads them and never writes them: the study\'s per-endpoint '
                 'timeout_seconds is applied to the resolved Endpoint value by dataclasses.replace '
                 'at provider construction, so the registry file itself is untouched and the plans '
                 'of other studies that pin the same bytes stay valid. A change to either file '
                 'mints a new plan_id (PLAN \u00a713).'),
    }


# ---------------------------------------------------------------- build

def load_artifact(arm: str, node: str) -> tuple[dict, str, str]:
    rel = f'artifacts/daily/{ARMS[arm]}/cycle01/{node}.json'
    path = OCC / rel
    raw = path.read_bytes()
    return json.loads(raw), sha(raw), (Path('experiments/diagnostics/H005-open-prose-commitments/occurrence-01') / rel).as_posix()


def build_arm(arm: str, h005: dict) -> dict:
    account, account_sha, account_rel = load_artifact(arm, 'account')
    rival, rival_sha, rival_rel = load_artifact(arm, 'rival')
    objection, objection_sha, objection_rel = load_artifact(arm, 'objection')

    coord_label = label(objection['coordinate'])
    body, commitments = objection['body'], objection['commitments']

    body_table = RU.FCL_BODY if arm == 'fcl' else RU.PROSE_BODY
    recoded_body, body_rows = recode_prose_document(body, body_table, 'B')

    if arm == 'fcl':
        recoded_commitments, commitment_rows = recode_fcl_commitments(commitments, RU.FCL_FIELDS)
        carrier_body = wrap(body)
        carrier_commitments = carrier_fcl_commitments(commitments)
        commitments_normaliser = 'canonical_fcl'
        norm_original = canonical_fcl(commitments)
        norm_carrier = canonical_fcl(carrier_commitments)
    else:
        recoded_commitments, commitment_rows = recode_prose_document(
            commitments, RU.PROSE_COMMITMENTS, 'C')
        carrier_body = wrap(body)
        carrier_commitments = bulletise(commitments)
        commitments_normaliser = 'normalise_prose'
        norm_original = normalise_prose(commitments)
        norm_carrier = normalise_prose(carrier_commitments)

    if normalise_prose(carrier_body) != normalise_prose(body):
        raise SystemExit(f'CARRIER_BODY_NOT_CONTENT_IDENTICAL {arm}')
    if norm_original != norm_carrier:
        raise SystemExit(f'CARRIER_COMMITMENTS_NOT_CONTENT_IDENTICAL {arm}')
    if carrier_body == body and carrier_commitments == commitments:
        raise SystemExit(f'CARRIER_NOT_DISTURBED {arm}')
    if normalise_prose(recoded_body) == normalise_prose(body):
        raise SystemExit(f'RECODING_IS_IDENTITY {arm}')
    if arm == 'fcl' and fcl_structure(recoded_commitments) != fcl_structure(commitments):
        raise SystemExit('RECODING_CHANGED_FCL_STRUCTURE')

    def case(case_body: str, case_commitments: str) -> dict:
        return {
            'body': case_body,
            'commitments': case_commitments,
            'body_sha256': tsha(case_body),
            'commitments_sha256': tsha(case_commitments),
            'objection_projection': projection(
                'objection', 'both', coordinate_label=coord_label,
                artifact_id=objection['artifact_id'], body=case_body,
                commitments=case_commitments, delivery=objection['delivery_status'],
                envelope=objection['envelope_status']),
        }

    cases = {
        'original': case(body, commitments),
        'recoding': case(recoded_body, recoded_commitments),
        'carrier': case(carrier_body, carrier_commitments),
        'control': {'body': None, 'commitments': None, 'body_sha256': None,
                    'commitments_sha256': None,
                    'objection_projection': absent_projection('objection', 'both')},
    }
    for name in cases:
        cases[name]['objection_projection_sha256'] = tsha(cases[name]['objection_projection'])
    if cases['original']['objection_projection'] != projection(
            'objection', 'both', coordinate_label=coord_label,
            artifact_id=objection['artifact_id'], body=body, commitments=commitments,
            delivery=objection['delivery_status'], envelope=objection['envelope_status']):
        raise SystemExit('ORIGINAL_PROJECTION_UNSTABLE')

    frozen = {}
    for name, artifact, art_sha, rel in (('account', account, account_sha, account_rel),
                                         ('rival', rival, rival_sha, rival_rel)):
        frozen[name] = {
            'view': 'both',
            'source_path': rel,
            'source_file_sha256': art_sha,
            'artifact_id': artifact['artifact_id'],
            'body_sha256': artifact['body_sha256'],
            'commitments_sha256': artifact['commitments_sha256'],
            'public_text_sha256': artifact['public_text_sha256'],
            'delivery_status': artifact['delivery_status'],
            'envelope_status': artifact['envelope_status'],
            'projection': projection(name, 'both', coordinate_label=label(artifact['coordinate']),
                                     artifact_id=artifact['artifact_id'], body=artifact['body'],
                                     commitments=artifact['commitments'],
                                     delivery=artifact['delivery_status'],
                                     envelope=artifact['envelope_status']),
        }
        frozen[name]['projection_sha256'] = tsha(frozen[name]['projection'])

    return {
        'source_arm': ARMS[arm],
        'policy_key': 'formal_instruction' if arm == 'fcl' else 'prose_instruction',
        'artifact_addresses': {
            'objection': objection['artifact_id'],
            'account': account['artifact_id'],
            'rival': rival['artifact_id'],
            'truncation_chars': 16,
            'note': ('The content addresses the three projections put in front of the responder. '
                     'A cross-document reference in the successor is attributed to a document only '
                     'when its prefix is one of these addresses, that address truncated to its first '
                     '16 hex characters (the form the real H005 response node emitted), or the '
                     'source name itself. A reference with no prefix is unresolved and stays in the '
                     'bare-token channel (FW5:634).'),
            'source_names': ['objection', 'account', 'rival'],
        },
        'record_ids_by_document': {
            'objection': (fcl_structure(commitments)['record_ids'] if arm == 'fcl' else None),
            'account': (fcl_structure(account['commitments'])['record_ids'] if arm == 'fcl' else None),
            'rival': (fcl_structure(rival['commitments'])['record_ids'] if arm == 'fcl' else None),
        },
        'objection_source': {
            'source_path': objection_rel,
            'source_file_sha256': objection_sha,
            'coordinate': objection['coordinate'],
            'coordinate_label': coord_label,
            'artifact_id': objection['artifact_id'],
            'body_sha256': objection['body_sha256'],
            'commitments_sha256': objection['commitments_sha256'],
            'public_text_sha256': objection['public_text_sha256'],
            'delivery_status': objection['delivery_status'],
            'envelope_status': objection['envelope_status'],
            'record_ids': (fcl_structure(commitments)['record_ids'] if arm == 'fcl' else None),
        },
        'frozen_inputs': frozen,
        'cases': cases,
        'recoding': {
            'authored_by': 'study designer, offline, before dispatch; no model call produced it',
            'unit_definition': ("prose documents: sentences produced by re.split(r'(?<=[.!?])\\\\s+', paragraph.strip()), "
                                "paragraphs split on '\\n\\n'; FCL-1 documents: the same sentence split applied to each "
                                'string field (text, scope, grounds, bearing, action, consequence) of each record'),
            'reconstruction': ("recoded document = paragraphs of units joined by ' ', paragraphs joined by '\\n\\n' "
                               '(prose) / original record and key order re-serialised with separators (",",":") (FCL-1); '
                               'the same reconstruction applied to the original units reproduces the original bytes'),
            'rule': {
                'R1': ('SYNONYM - lexical substitution preserving reference and illocutionary force. '
                       'A contraction and its expansion ("I\'d" / "I would", "can\'t" / "cannot") are the '
                       'same lexical items in the same order with the same modal force; that alternation is '
                       'orthographic and is recorded under R1 rather than as an operation of its own.'),
                'R2': ('CONSTITUENT-ORDER - reordering of constituents (clauses, phrases, '
                       'adverbials) inside one unit. Broadened 2026-09-14 from '
                       '"reordering of clauses": the label was already carried by units that '
                       'front a PP or an adverbial, and the narrower wording made those labels '
                       'false. The restriction is unchanged - the reordering stays inside one '
                       'unit, and it may not be used for an operation on an NP head.'),
                'R3': 'VOICE - active/passive or verbal/nominal alternation',
                'R4': ('DEIXIS - demonstrative <-> explicit antecedent inside one unit. Applicable ONLY where '
                       'the demonstrative has a unique antecedent inside the same paragraph, and the uniqueness '
                       'argument is recorded in the unit row. Re-checked 2026-09-14: no unit of either document '
                       'satisfies that restriction, so R4 is declared and not exercised.'),
                'R5': 'CONNECTIVE - substitution of an equivalent discourse connective',
            },
            'hedge_markers': list(HEDGE_MARKERS),
            'hedge_marker_limits': (
                'What the counter cannot see. The check refuses a change in the COUNT of a declared '
                'marker family inside a unit, and nothing else. It is blind to illocutionary and '
                'evaluative force carried by ordinary predicates, and blind to which constituent a '
                'preserved marker attaches to. The independent spot-check of 2026-09-14 found it '
                'passing all 85 units while missing: "consistent with" -> "fit" (a bare compatibility '
                'relation loosened into a confirmatory one); "downweight" -> "discount"; "issue" -> '
                '"point"; "fine" -> "unobjectionable" (an un- litotes is not in the NEGATION family); '
                '"or" -> "and" under a negation, which admits a not-both reading the original excludes; '
                'and get-passive -> be-passive. Changes of that kind are caught only by reading. The '
                '85-row correspondence table is published so the reading can be disputed row by row, '
                'and the two-reviewer re-read recorded in FIXES.md - the 2026-09-14 constituent re-read '
                'and the independent spot-check that followed it - is the record of its having been '
                'done. Every case listed here was reverted, not licensed.'),
            'hedge_marker_note': (
                'Declared hedge/modal marker families. `prepare` counts each family in the original and in the '
                'recoded text of every unit, after expanding contractions, and refuses the material if any '
                'count differs (RECODING_HEDGE_FORCE_CHANGED). This is the mechanical half of the '
                '"hedge force preserved" invariant; the semantic half is the published unit table.'),
            'invariants': [
                'unit count, unit order and unit boundaries preserved; no cross-unit move',
                'quoted material reproduced verbatim',
                'FCL-1 record ids, types, uptake and every reference array unchanged',
                'no proposition added, dropped, strengthened or weakened; hedge force preserved, checked per '
                'unit as an exact count of every declared hedge/modal marker family',
                'criticism constituents preserved: target z, alleged defect delta, grounds g, bearing (FW5:609)',
                'no information-structure operation beyond the topic/focus reassignment intrinsic to R3 '
                '(active/passive alternation): no clefting, pseudo-clefting, topicalisation, equative '
                'inversion, existential-`there` insertion or deletion, subordination<->coordination, '
                'assertion<->presupposition - and no determiner or definiteness operation of its own: no '
                'the<->a, the<->this/that or bare<->determined change to an otherwise unchanged referring '
                'expression. Neither is in the declared rule set, so a unit that needed one was reverted to '
                'the simplest declared operation instead. Two intrinsic consequences are excluded rather '
                'than denied, because the material exercises both: R3 itself reassigns topic and focus '
                '(16 fcl and 14 prose units apply a voice or nominal alternation), and an R1 lexical '
                'paraphrase or an R3 verbal<->nominal alternation carries its own determiner with it '
                '("falling recurrence" -> "a fall in recurrence", "presenting that sequence" -> "the '
                'presentation of that sequence", "being able to hold" -> "the ability to hold"). 26 units '
                'show a determiner-token delta of that second kind; none is a determiner operation applied '
                'on its own, and every unit that had applied one was reverted',
            ],
            'not_exercised': [
                'cross-unit sentence re-ordering: available but deliberately unused, because unit order can '
                'carry argumentative dependence and its preservation makes the correspondence table checkable '
                'unit by unit. Recorded as an open question for root.',
                'R4 DEIXIS: declared, and not exercised anywhere. Under its uniqueness restriction no '
                'demonstrative in either document has a unique antecedent inside its own paragraph, so every '
                'unit that had applied a deixis operation was reverted at the 2026-09-14 re-read.',
                'information structure and determiner/definiteness: not declared as rules (no R6, no R7) and '
                'not used. This list is exhaustive as of the 2026-09-14 spot-check closure, which is what '
                'the earlier version of it was not. Reverted in the fcl document: B.P1.S1, B.P2.S3, '
                'B.P2.S7, B.P3.S2, B.P3.S3, B.P4.S1, B.P4.S2, B.P4.S4, B.P5.S2, B.P6.S3, '
                'K.o1.text.S1, K.o3.text.S1, K.o3.text.S2, K.o3.bearing.S1, K.c2.text.S1. '
                'Reverted in the prose document: B.P1.S1, B.P2.S2, B.P2.S3, B.P2.S4, B.P3.S1, '
                'B.P3.S4, B.P3.S7, B.P4.S1, B.P4.S2, B.P4.S3, B.P4.S4, B.P5.S1, B.P5.S3, C.P2.S1, '
                'C.P3.S1, C.P3.S2, C.P4.S1, C.P4.S3, C.P5.S2. The three units the '
                'spot-check recorded as outright violations of the declared rule set are inside that list '
                '- fcl K.o1.text.S1 (existential-`there` inserted, in record o1\'s own `text` field), fcl '
                'B.P4.S1 (existential-`there` deleted) and fcl B.P4.S2 (definite possessive predicate '
                'nominal turned into a bare plural, plus an equative->predicational shift) - as are the '
                'fronted-frame-adjunct (fcl B.P3.S2), NP-head-switch (fcl B.P3.S3), coordinated-definite-NP '
                '(fcl B.P5.S2) and cataphor (prose B.P4.S1) cases. Each was reverted to the simplest '
                'declared operation rather than licensed by a new rule, because the content-preservation '
                'argument for each is not clear-cut.',
                'evaluative and relational predicate substitution: not licensed by R1, which is restricted '
                'to substitutions preserving reference AND illocutionary force, and not declared as a rule '
                'of its own. Reverted at the spot-check closure: fcl B.P2.S7 ("hold" restored to "bind"), '
                'B.P3.S1 ("adopts"/"discounts" restored to "treats"/"gives less weight to"), B.P3.S4 '
                '("fit" restored to "be consistent with"), B.P4.S1 ("point" restored to "issue"), B.P4.S3 '
                '("unobjectionable" restored to "fine"), B.P5.S1 ("relegates to second place" restored to '
                '"treats as secondary"), K.o1.text.S2 ("discounted" restored to "given less weight"), '
                'K.c2.text.S1 ("and" restored to "or" under the negation, by leaving the clause active), '
                'and prose B.P2.S4 ("describes" restored to "is a description of"). None of these is '
                'visible to the hedge/modal counter; see hedge_marker_limits.',
            ],
            'units': body_rows + commitment_rows,
            'unit_count': len(body_rows) + len(commitment_rows),
        },
        'carrier': {
            'operations': (
                ['body: paragraphs hard-wrapped to 72 columns (whitespace only)',
                 'commitments: FCL-1 document re-serialised with indent=2, keys sorted alphabetically, '
                 'records array reversed, uptake array reversed']
                if arm == 'fcl' else
                ['body: paragraphs hard-wrapped to 72 columns (whitespace only)',
                 'commitments: each paragraph rendered as one "- " bullet item, hard-wrapped to 68 columns '
                 'with two-space continuation indent; sentence order unchanged']),
            'grain_declaration': (
                'FCL-1 content is the set of records keyed by id (each a field->value map), the set of uptake ids '
                'and the language tag; array order, key order and whitespace are carrier. Prose content is the '
                'sequence of whitespace-separated word tokens; line breaks, indentation and bullet markers are '
                'carrier. This declaration is itself a criticisable interpretation claim (SEMANTIC_GUIDE, '
                '"Declare the interpretation before the evidence").'),
            'normalisation': {
                'body': 'normalise_prose: strip leading bullet markers per line, collapse whitespace runs to one space, strip',
                'commitments': commitments_normaliser,
            },
            'proof': {
                'body_original_normalised_sha256': tsha(normalise_prose(body)),
                'body_carrier_normalised_sha256': tsha(normalise_prose(carrier_body)),
                'body_equal': normalise_prose(body) == normalise_prose(carrier_body),
                'commitments_original_normalised_sha256': tsha(norm_original),
                'commitments_carrier_normalised_sha256': tsha(norm_carrier),
                'commitments_equal': norm_original == norm_carrier,
                'body_bytes_differ': carrier_body != body,
                'commitments_bytes_differ': carrier_commitments != commitments,
            },
        },
    }


def main() -> int:
    h005_raw = (H005 / 'material.json').read_bytes()
    h005 = json.loads(h005_raw)
    problem = next(p for p in h005['problems'] if p['id'] == 'daily')
    node = next(n for n in h005['templates']['fork5']['nodes'] if n['id'] == 'response')
    if [b['source'] for b in node['inputs']] != ['account', 'objection', 'rival']:
        raise SystemExit('NODE_INPUT_ORDER_CHANGED')

    fw5 = REPO / 'docs/sources/FW5-explanatory-construction.md'
    material = {
        'schema': 'minireason.c001.material.v1',
        'study': 'C001-contrast-triple',
        'question': (
            'At one responder node - the fork5 `response` node, instruction and non-objection inputs frozen '
            'from the H005 material and occurrence-01 - does the successor\'s authored commitment surface '
            'differ against a no-objection control, and NOT under a content-preserving recoding of the '
            'objection, and NOT under a carrier disturbance at fixed content? (FW5:630 contrast contract, '
            'redirected from the judge to the responder.)'),
        'claim_ceiling': (
            'One system, one problem, one respect. Consistent-with, never a reason-use witness (FW5:628). '
            'An unresolved cell stays unresolved (FW5:634).'),
        'node': {
            'template_id': 'fork5',
            'node_id': 'response',
            'instruction': node['instruction'],
            'instruction_sha256': tsha(node['instruction']),
            'inputs': node['inputs'],
            'varying_input': {'source': 'objection', 'view': 'both'},
            'frozen_inputs': ['account', 'rival'],
        },
        'problem': {'id': problem['id'], 'prose': problem['prose'],
                    'prose_sha256': tsha(problem['prose'])},
        'system_common': h005['system'],
        'policies': {'fcl': h005['formal_instruction'], 'prose': h005['prose_instruction']},
        'public_contract': (
            'Return one JSON object with exactly two string fields: "body" and '
            '"commitments". Write the actual commitments separately; do not copy '
            'the body into that field as a storage shortcut.'),
        'envelope': ('## What to return\nA JSON object carrying "body" and "commitments". '
                     'Both are strings and nothing else is required.'),
        'render': {
            'rule': 'direct_explicit_views',
            'shape': ['## Node <node_id>', '<instruction>', '## Original problem', '<problem prose>',
                      '## Selected input account', '<account projection>',
                      '## Selected input objection', '<objection projection for this case>',
                      '## Selected input rival', '<rival projection>', '<envelope>'],
            'join': "sections joined by '\\n\\n'",
            'note': ('Reproduces the non-Mini branch of tools/multicycle_commitment_study.py `render_node`. '
                     'The canonical Mini reducer render is deliberately not used: its port headers carry a '
                     'content-addressed artifact id, which would vary across cases as an uncontrolled carrier '
                     'difference.'),
        },
        'arms': {arm: build_arm(arm, h005) for arm in ARMS},
        'cases': ['original', 'recoding', 'carrier', 'control'],
        'replicates': 5,
        'seeds': [1, 2, 3, 4, 5],
        'endpoints': [
            {'id': 'deepseek-flash', 'slug': 'deepseek-flash', 'model': 'deepseek-flash',
             'key_env': 'DEEPSEEK_API_KEY', 'family': 'deepseek', 'native': False,
             'honors_seed': None, 'max_tokens': 8192, 'timeout_seconds': 180,
             'reachable_at_smoke_test': True,
             'note': 'Registry name in src/minireason/data/endpoints.json. Keeps the registry\'s own 180-second wall-clock timeout: it sends no reasoning on the wire and took no read timeout in F001. Seed support unverified; '
                     'the seed is sent and every record states seed_requested, seed_sent and whether '
                     'the provider response echoed a seed.'},
            {'id': 'ollama/gpt-oss-120b', 'slug': 'ollama-gpt-oss-120b', 'model': 'gpt-oss:120b',
             'key_env': 'OLLAMA_API_KEY', 'family': 'ollama-cloud/gpt-oss', 'native': False,
             'honors_seed': True, 'reachable_at_smoke_test': True,
             'max_tokens': 32768, 'timeout_seconds': 600,
             'note': 'OpenAI-compatible chat path. Seed honoured (smoke test). Emits reasoning by '
                     'default, which counts against max_tokens.'},
            {'id': 'ollama/qwen3.5-397b', 'slug': 'ollama-qwen3.5-397b', 'model': 'qwen3.5:397b',
             'key_env': 'OLLAMA_API_KEY', 'family': 'ollama-cloud/qwen', 'native': False,
             'honors_seed': True, 'reachable_at_smoke_test': True,
             'max_tokens': 32768, 'timeout_seconds': 600,
             'note': 'OpenAI-compatible chat path. Seed honoured (smoke test).'},
            {'id': 'ollama/glm-5.3', 'slug': 'ollama-glm-5.3', 'model': 'glm-5.3',
             'key_env': 'OLLAMA_API_KEY', 'family': 'ollama-cloud/glm', 'native': False,
             'honors_seed': True, 'reachable_at_smoke_test': True,
             'max_tokens': 32768, 'timeout_seconds': 600,
             'note': 'OpenAI-compatible chat path. Seed honoured (smoke test). Wall-clock timeout 600 s: this family took one of the two read timeouts of F001 occurrence-07 (mini_fcl/objection, elapsed_ms 180368 at a 180-second setting) under REC-20260914-T.'},
            {'id': 'ollama/kimi-k3', 'slug': 'ollama-kimi-k3', 'model': 'kimi-k3',
             'key_env': 'OLLAMA_API_KEY', 'family': 'ollama-cloud/kimi', 'native': False,
             'honors_seed': True, 'reachable_at_smoke_test': True,
             'max_tokens': 32768, 'timeout_seconds': 600,
             'note': 'OpenAI-compatible chat path. Seed honoured (smoke test). Wall-clock timeout 600 s: this family took one of the two read timeouts of F001 occurrence-08 (mini_fcl/carry, elapsed_ms 180456 at a 180-second setting) under REC-20260914-T.'},
            {'id': 'ollama/gemma4-31b', 'slug': 'ollama-gemma4-31b', 'model': 'gemma4:31b',
             'key_env': 'OLLAMA_API_KEY', 'family': 'ollama-cloud/gemma', 'native': False,
             'honors_seed': True, 'reachable_at_smoke_test': True,
             'max_tokens': 32768, 'timeout_seconds': 600,
             'note': 'OpenAI-compatible chat path. Seed honoured (smoke test).'},
        ],
        'ceilings': {
            'max_tokens': {'deepseek-flash': 8192,
                           'ollama/gpt-oss-120b': 32768,
                           'ollama/qwen3.5-397b': 32768,
                           'ollama/glm-5.3': 32768,
                           'ollama/kimi-k3': 32768,
                           'ollama/gemma4-31b': 32768},
            'max_tokens_authorised_maximum': 32768,
            'max_tokens_policy': (
                'max_tokens is declared PER ENDPOINT, not once for the study, and the value for '
                'each endpoint is frozen in endpoints[].max_tokens as well as here; `prepare` '
                'refuses unless the two agree and unless every built payload carries its own '
                "endpoint's value (CEILING_NOT_APPLIED). deepseek-flash keeps 8192: it sends no "
                'reasoning on the wire, and 8192 was ample for it. The five Ollama endpoints are '
                'raised to 32768 BEFORE dispatch, on live evidence published under REC-20260914-S '
                'in experiments/diagnostics/F001-fork5-multifamily (occurrence-04, ollama/glm-5.3; '
                'occurrence-05, ollama/kimi-k3): at max_tokens 8192 five nodes returned '
                'INCOMPLETE_GENERATION with finish_reason "length", completion_tokens 8192 and no '
                'content at all - the whole ceiling went to reasoning - and two further nodes came '
                'back PARTIAL. Those two families emit reasoning by default and the reasoning '
                'tokens count against max_tokens. Raising the ceiling does NOT manipulate '
                'reasoning: temperature, thinking and reasoning_effort are still never sent, the '
                "endpoint default still decides whether and how much it reasons, and the study's "
                'own reasoning policy is unchanged. It buys the reply room to exist beside the '
                'reasoning, nothing more. A cell that hits even the raised ceiling is still a '
                'PARTIAL or a refusal, is still marked unresolved and is still compared against '
                'nothing (partial_delivery_rule; FW5:634).'),
            'timeout_seconds': {'deepseek-flash': 180,
                                'ollama/gpt-oss-120b': 600,
                                'ollama/qwen3.5-397b': 600,
                                'ollama/glm-5.3': 600,
                                'ollama/kimi-k3': 600,
                                'ollama/gemma4-31b': 600},
            'timeout_seconds_authorised_maximum': 600,
            'timeout_seconds_policy': (
                'timeout_seconds is declared PER ENDPOINT, exactly as max_tokens is, and the '
                "value for each endpoint is frozen in endpoints[].timeout_seconds as well as "
                'here. It is a WALL-CLOCK READ TIMEOUT on the socket, not a payload field: no '
                'new parameter is sent, no payload byte changes, and the plan_id-bearing '
                'request bytes are the same bytes they would be at any timeout. The driver '
                "applies it to the registry Endpoint through `dataclasses.replace` at provider "
                'construction (resolve_endpoint), so src/minireason/data/endpoints.json is '
                'NEVER edited: that file is published, pinned here in transport_pins, and '
                "pinned by other studies' plans, and a study that rewrote it would invalidate "
                'them. prepare, run and audit all refuse unless the frozen plan, the material, '
                "the call spec, the request record, the receipt and the transport's own "
                'settings view carry the same value (TIMEOUT_NOT_APPLIED). deepseek-flash '
                "keeps the registry's own 180 s. The five Ollama endpoints carry 600 s, which "
                "is the transport's OWN validation maximum: "
                'minireason.provider_openai_compat.Endpoint.__post_init__ admits '
                '1..600 seconds and refuses anything else, so 600 is a bound this study '
                'reaches rather than one it invents. The raise is made BEFORE dispatch, on '
                'live evidence published under REC-20260914-T in '
                'experiments/diagnostics/F001-fork5-multifamily. Two nodes of that run failed, '
                'and both failed this way: occurrence-07 (ollama/glm-5.3) '
                'responses/daily/mini_fcl/cycle01/objection.json, failure_code '
                'TRANSPORT_OR_RESPONSE_ERROR, whose provider record '
                'provider/daily/mini_fcl/cycle01/objection/call-0001.response.json carries '
                'error "The read operation timed out", elapsed_ms 180368 and '
                'settings.timeout_seconds 180; and occurrence-08 (ollama/kimi-k3) '
                'responses/daily/mini_fcl/cycle01/carry.json with the same failure_code, whose '
                'provider record carries the same error at elapsed_ms 180456 against the same '
                '180-second setting. Both were sent at max_tokens 32768; both returned no '
                'finish_reason, no usage and no content; neither is INCOMPLETE_GENERATION and '
                'neither is a ceiling truncation - finish_reason "length" occurs ZERO times in '
                'either occurrence, and the largest single completion there was 16871 tokens. '
                'What those two calls met was the fixed 180-second wall clock, which did not '
                'move when the completion ceiling moved. Raising it manipulates no reasoning: '
                'temperature, thinking and reasoning_effort are still never sent, the endpoint '
                'default still decides whether and how much it reasons, and the study\'s own '
                'reasoning policy is unchanged; a longer permitted generation is simply given '
                'the wall-clock room to arrive. Its cost is recorded: the six endpoints no '
                'longer share one timeout, so a difference between deepseek-flash and an '
                'Ollama endpoint has one more uncontrolled difference behind it. A call that '
                'exceeds even 600 seconds is still a refusal recorded with its failure code '
                '(TRANSPORT_OR_RESPONSE_ERROR), still compared against nothing, and NO CELL IS '
                'RESCUED by the raise.'),
            'automatic_retries': 0,
            'max_concurrent_per_key': 5,
            'temperature': 'provider-default',
            'response_format': {'type': 'json_object'},
            'native_reasoning': 'not manipulated; endpoint default; recorded as reported or unknown',
        },
        'seed_policy': (
            'Send seed=<replicate> to every endpoint whose declared honors_seed is true or null '
            '(unverified); send no seed only where honors_seed is declared false. Every call record '
            'states seed_requested, seed_sent, honors_seed and seed_echoed_in_response. Ollama honours '
            'seed (smoke test); DeepSeek seed support is unverified, so its replicates are recorded as '
            'independent samples whose seed effect is unestablished.'),
        'envelope_unwrap': {
            'reason': ('Ollama cloud accepts response_format json_object but does not enforce it: a '
                       'model may fence the JSON or return invalid JSON, and most Ollama models emit '
                       'reasoning by default, which counts against max_tokens. H005 ran one endpoint '
                       'that did enforce it, so its decoder needed no unwrap.'),
            'steps': [
                '1. strict json.loads of the delivered content; if it yields {"body","commitments"} '
                'of strings, no repair is recorded',
                '2. otherwise strip ONE outer code fence (```lang ... ```) and retry the strict parse; '
                'records envelope_repairs += ["strip_outer_code_fence"]',
                '3. otherwise retry with json.loads(strict=False) (control characters admitted inside '
                'strings); records envelope_repairs += ["json_strict_false"]',
                '4. otherwise the envelope is OPAQUE and the whole delivered text is kept as the body',
            ],
            'guarantees': [
                'raw delivered bytes are preserved untouched in responses/<...>.txt and in the '
                'write-once provider record',
                'every call records envelope_repairs and strict_parse_would_succeed',
                'no other repair is ever applied to content',
            ],
        },
        'partial_delivery_rule': (
            'A PARTIAL delivery (finish_reason "length" at the endpoint\'s own declared max_tokens '
            'ceiling - 8192 for deepseek-flash, 32768 for the five Ollama endpoints) yields a '
            'truncated commitment surface. Such a cell is marked unresolved in the evidence table and '
            'is not compared against any other case (FW5:634; EXPERIMENT_METHOD operational-failure '
            'table). A delivery that returns no content at all because the ceiling went entirely to '
            'reasoning is a refusal (INCOMPLETE_GENERATION), recorded with its failure code and '
            'likewise compared against nothing. Raising the Ollama ceiling makes those outcomes less '
            'likely; it does not change how they are read.'),
        'planned_calls': 4 * 5 * 6 * 2,
        'reading_rule': READING_RULE,
        'transport_pins': transport_pins(),
        'source_pins': {
            'docs/sources/FW5-explanatory-construction.md': sha(fw5.read_bytes()),
            'experiments/diagnostics/H005-open-prose-commitments/material.json': sha(h005_raw),
        },
    }
    for arm in ARMS:
        block = material['arms'][arm]
        material['source_pins'][block['objection_source']['source_path']] = \
            block['objection_source']['source_file_sha256']
        for name in ('account', 'rival'):
            material['source_pins'][block['frozen_inputs'][name]['source_path']] = \
                block['frozen_inputs'][name]['source_file_sha256']

    OUT.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(material, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    OUT.write_text(raw, encoding='utf-8')

    # The published correspondence table is rendered from the bytes just written, by the
    # driver's own renderer - the same function `prepare` calls - so the table and the
    # material cannot disagree about a unit, a rule label or an invariant.
    sys.path.insert(0, str(DRIVER_DIR))
    import contrast_triple_study as CTS  # noqa: E402
    table = CTS.render_recoding_table(json.loads(raw))
    TABLE.write_text(table, encoding='utf-8')

    print(json.dumps({'written': str(OUT), 'bytes': len(raw.encode()),
                      'sha256': tsha(raw),
                      'table': str(TABLE), 'table_sha256': tsha(table),
                      'units': {a: material['arms'][a]['recoding']['unit_count']
                                for a in ARMS}}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
