"""H005 multi-provider fork v3: per-arm wall clock beside the per-arm ceiling.

V3 PROVENANCE.  This file is a byte copy of
``tools/multicycle_commitment_study_multi_v2.py`` at sha256
``8f7eb9d73e8c497f6a2aabf826a8409bb3c60682b36aaa361f650a9e870adbd0``
with seven declared differences, in eight hunks, and no others.  Each one is
marked ``# V3:`` in
the source, and ``tests/test_multicycle_commitment_study_multi_v3.py`` proves
the claim: it normalises this module docstring away, diffs the two files and
asserts that the only hunks are the ones listed here, line for line, comments
included.

The motive is one published fact.  F001 occurrences 07 and 08 raised the
completion ceiling to 32,768 under v2 and were then refused by the wall clock:
both of that run's two failures are ``TRANSPORT_OR_RESPONSE_ERROR`` -- ``"The
read operation timed out"`` at 180,368 ms and 180,456 ms against the endpoint
record's 180 seconds -- neither of them a ceiling truncation, and the truncation
rule then ended those arms.  v2's own header says why the runner could not
answer: "the timeout is NOT [a per-arm declaration] - it is the endpoint
record's and no arm declaration can change it."  C001 occurrence-02 met the same
wall in the contrast driver and resolved it the way this file does: declare the
clock beside the ceiling, apply it to the resolved ``Endpoint`` value with
``dataclasses.replace``, and never write ``src/minireason/data/endpoints.json``,
which is a pinned published file that other plans hash.

(a) This provenance block, which is the only change to the module docstring
    besides (g).
(b) ``replace`` joins the ``dataclasses`` import.  It is the one new name this
    file uses and it is the transport's own idiom for a per-call endpoint value.
(c) ``MAX_TIMEOUT = 600``, mirrored from the transport, not invented:
    ``provider_openai_compat.Endpoint.__post_init__`` and this file's own
    ``EndpointSettings.__post_init__`` both admit ``1 <= n <= 600`` and refuse
    601.  No DEFAULT_TIMEOUT constant is added, because the default is not a
    module figure: it is whatever the endpoint record itself declares, so an arm
    that declares no clock is settled exactly as v2 settles it.
(d) ``ARM_OPTIONAL`` gains ``timeout_seconds``.
(e) ``validate_arms`` reads, bounds and freezes it -- two hunks, one for each.
    The key is written into the
    frozen arm ONLY where the declaration carries one, so a v3 plan built from a
    v2 arms.json is v2's plan in every field but the two runner digests and the
    ``plan_id`` they feed.
(f) ``settings_for`` takes the arm's declared clock where there is one and the
    endpoint record's otherwise.  Nothing downstream needs a change to record
    it: ``EndpointSettings.to_dict()`` already carries ``timeout_seconds`` and is
    already compared field for field against the provider's own settings view by
    ``decode_contribution`` and ``read_terminal``, so a clock that was declared
    and not applied is already a custody refusal.
(g) ``plan_body``'s comment said the timeout is read from the endpoint and no
    arm declaration can change it.  That sentence is false of this file, so it
    is rewritten.  ``plan["ceilings"]`` itself is untouched: it already surfaces
    the effective clock per arm, and now surfaces the declared one.
(h) ``send_wave`` applies the arm's clock to the resolved ``Endpoint`` by
    ``dataclasses.replace`` before the provider is constructed, and refuses
    ``TIMEOUT_NOT_APPLIED`` if the value the transport is about to receive is
    not the declared one -- ``replace`` is an external function on an external
    class, and an endpoint type that clamps or ignores the field would
    otherwise spend the call and fail custody afterwards.  ``send_round`` needs no change: it
    dispatches through ``send_wave``.

Nothing else differs.  Node topologies, view projection text, payload bytes,
``write_new``, ``plan_id``/``verify``, waves, attempts, NO_REPLAY, artifacts,
traces, the provider record layout, the per-key gate and the publication check
are v2's bytes, which are v1's.  This file's own sha256 is what it writes as
``runner_sha256`` and ``helper_sha256``, so every plan built here carries a
``plan_id`` no v1 or v2 plan can collide with: a v3 occurrence is a separate
identity, not a re-run.

--- v2's own header follows, unchanged ---

V2 PROVENANCE.  This file is a byte copy of
``tools/multicycle_commitment_study_multi.py`` at sha256
``a56fed415bd72395470f40c18d9985ec6fcde8a851662006a9b6fecbfe57ec80``
with four declared differences and no others.  Each one is marked ``# V2:`` in
the source, and ``tests/test_multicycle_commitment_study_multi_v2.py`` proves
the claim: it normalises this module docstring away, diffs the two files and
asserts that the only hunks are the ones listed here.

(a) This provenance block, which is the only addition to the module docstring
    besides (d).
(b) The completion-ceiling constant.  v1's ``CAP = 8192`` did two jobs - it was
    the bound ``validate_arms`` enforced on a declared per-arm ``max_tokens``,
    and it was the default an arm that declares none receives.  Only the BOUND
    moves.  ``MAX_CEILING = 393216`` is the provider's own bound, mirrored from
    ``minireason.provider_openai_compat._RecordedCaller._validate_call_args``,
    which refuses any ``max_tokens`` outside ``1 <= n <= 393216``, and
    ``validate_arms`` now accepts any per-arm ceiling in ``1..MAX_CEILING``.
    ``DEFAULT_CEILING = 8192`` keeps v1's value, so an arm that declares no
    ``max_tokens`` is settled exactly as v1 settles it and the raised bound is
    the only behavioural difference.  (v1's ``EndpointSettings.__post_init__``
    already admitted the provider bound; ``validate_arms`` was the only place
    that capped an arm at 8,192.)
(c) ``manifest_for`` takes the occurrence's frozen arm mapping and derives
    ``cycles.completion_tokens_per_call`` and ``cycles.max_completion_tokens``
    from the ceilings the arms actually declare instead of from the module
    constant.  A manifest is per TEMPLATE and is shared by every arm, so the
    derivation is the maximum declared per-arm ceiling of the occurrence: the
    smallest figure that is a true upper bound for every arm of it, a pure
    function of the frozen ``arms.json``, and identical to v1's figure on any
    occurrence whose arms all sit at the default.  Without it, raising the
    constant alone would write a ceiling into every manifest that no arm asked
    for, and raising the bound alone would leave every manifest declaring 8,192
    while its arms ran higher.
(d) This docstring says v2; ``argparse`` prints it as the tool description.

Nothing else differs.  Node topologies, view projection text, payload bytes,
``write_new``, ``plan_id``/``verify``, waves, attempts, NO_REPLAY, artifacts,
traces, the provider record layout, the per-key gate and the publication check
are v1's bytes.  This file's own sha256 is what it writes as ``runner_sha256``
and ``helper_sha256``, so every plan built here carries a ``plan_id`` no v1
plan can collide with: a v2 occurrence is a separate identity, not a re-run.

--- v1's own header follows, unchanged ---

Forked from tools/multicycle_commitment_study.py at
9b8463bb33cbca131e050763720c12a0f68ffdad07cb4e25df666e17400d2a72 under this
session; differences listed below.

Every difference from the owner's runner is marked ``# MULTI:`` in the source.
The list, in the order the fork's own brief numbers them:

(a) ARMS is no longer a module constant.  Arms are declared per occurrence as a
    mapping ``arm_name -> {"surface": "prose"|"fcl", "kind":
    "bare"|"native"|"matched"|"mini", "endpoint": <endpoint name>}``, frozen in
    ``<occurrence>/arms.json`` and pinned into ``plan.json`` by
    ``arms_sha256``.  ``settings_for`` / ``payload_for`` / the dispatch are
    built from the arm's endpoint through ``minireason.provider_openai_compat``
    (``Endpoint``/``ENDPOINTS``, ``OpenAICompatProvider``, ``OfflineProvider``),
    whose write-once ``call-NNNN.request.json``/``.response.json`` records are
    the ones the H005 custody chain reads.  Thinking controls are emitted only
    for the ``deepseek`` family, because that module refuses them anywhere else;
    a ``native`` arm on any other family is refused when the plan is built.
(b) Concurrency is per credential, and the per-key ceiling is process-wide.
    Ready coordinates are grouped by ``key_env``: a wave carries at most
    ``key_cap`` of them per credential (five, or an endpoint's smaller
    ``max_concurrency``) and their sum in all, and every in-flight call is held
    by a module-level per-key gate (``key_gate``, mirroring
    ``provider_openai_compat.slots_for``) acquired BEFORE the attempt marker is
    written.  Wave construction is the first line and the gate is the second:
    the gate is what holds two occurrences spending one credential to five in
    flight between them, so one process may drive several occurrences together
    (``send-round``).
(c) ``check_published`` verifies HEAD against a configurable ref
    (``--publish-ref``; default the current branch's upstream) instead of a
    hardcoded ``origin/main``, and still byte-compares every required input
    path against the committed bytes.
(d) Study id and occurrence root are parameters (``--study
    experiments/diagnostics/<STUDY-ID>``); ``material.json`` may be a copy of
    H005's material carrying an extra ``study_id`` field.
(e) ``plan.json`` gains ``providers`` (endpoint records without keys),
    ``runner_sha256`` of this file, ``arms_sha256``, ``study_id`` and
    ``max_concurrent_requests_total``.
(f) Everything else is byte-identical to the owner's runner: node topologies,
    view projection text, ``write_new``, ``plan_id``/``verify``, waves,
    attempts, NO_REPLAY, artifacts, traces and the provider record layout, so
    that ``minireason.graph_import_h005.import_occurrence`` reads the result.
(g) One declared decode step, ``envelope_unwrap``, runs before the same strict
    shape check: strip ONE outer Markdown fence, then re-parse with
    ``strict=False``.  Ollama cloud accepts ``response_format: json_object``
    without enforcing it, so without this the fork would lose authored
    commitments in decoding on most families.  Nothing else is repaired, no
    field is reconstructed, the raw public text is stored and hashed unchanged,
    and an envelope no declared repair rescues is still OPAQUE.  The receipt
    records ``envelope_repairs`` and ``strict_parse_would_succeed`` per node,
    and the artifact record keeps the owner's field set exactly.  A fork
    occurrence's OPAQUE rate is therefore NOT comparable with H005
    occurrence-01; ``strict_parse_would_succeed`` is the comparable figure.
(h) The completion ceiling and the seed are per-arm declarations
    (``ARM_OPTIONAL``); the timeout is NOT - it is the endpoint record's and no
    arm declaration can change it.  All three are surfaced per arm in
    ``plan["ceilings"]``, the first two as declared and the third as read from
    the endpoint.  ``decode_contribution`` checks the arm's ceiling
    rather than a module constant.  Ollama honours ``seed``; DeepSeek declares
    none, so it stays null there.  ``finish_reason`` and ``usage`` are recorded
    per node, and a ceiling-truncated call is PARTIAL exactly as the owner's
    runner records it.
(i) Hidden reasoning is a custody failure only where the runner set a thinking
    control and set it to disabled - the DeepSeek family.  Every other family
    emits reasoning by default with no switch, so ``reasoning_content_present``
    is recorded per node instead of failing it; ``reasoning_content_persisted``
    remains a hard refusal.

(j) An occurrence may freeze a ``scope`` in its ``arms.json``
    (``{"problems": [...], "cycles": [...]}``), pinned into ``plan["scope"]``.
    ``ready_coordinates`` refuses any coordinate outside it
    (``SCOPE_EXCLUDED``), ``audit`` reads the scope and counts anything found
    outside it as ``out_of_scope``, and ``max_calls`` counts only the calls the
    scope admits - the full material envelope stays visible beside it as
    ``max_calls_envelope``.
(k) A receipt records ``failure_code`` beside ``failure_type``: the provider's
    own ``ProviderFailure.code`` (``HTTP_429``, ``KEY_MISSING``,
    ``TRANSPORT_OR_RESPONSE_ERROR``, ...), so a rate limit and a missing
    credential are distinguishable without opening the provider records.

No durable scheduler, semantic validator, automatic retry, or Git mutation is used.
Each cycle is a complete template invocation; nodes are individual model calls.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, replace   # V3 (b)
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
import threading

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / 'src'))
sys.path.insert(0, str(REPOSITORY))
from creib.forge.mini.kinds import Submission, read_submission
from creib.forge.mini.log import ARTIFACT_SUBMITTED, MiniState, apply_event, build_event
from creib.forge.mini.manifest import Stage, compile_manifest
from creib.forge.mini.runner import _store_artifact, render_brief
from minireason.provider import digest
from tools.multicycle_language_probe import MemoryBlobs

# MULTI (a): the owner's runner imports DeepSeek and a DeepSeek-locked Settings.
# The fork resolves both from the endpoint registry instead.  The import is
# deferred to `endpoints()` so that an offline occurrence can be initialized,
# verified, prepared and audited on a checkout where the concurrently built
# provider module has not landed yet.
PROVIDER_MODULE = 'minireason.provider_openai_compat'
PROVIDER_MODULE_PATH = 'src/minireason/provider_openai_compat.py'
ENDPOINT_REGISTRY_PATH = 'src/minireason/data/endpoints.json'

# MULTI (a): ARMS/BASELINE_ARMS were module constants naming the five H005 arms.
# They become the closed vocabularies an arm declaration is validated against.
SURFACES = ('prose', 'fcl')
KINDS = ('bare', 'native', 'matched', 'mini')
BASELINE_KINDS = ('bare', 'native')
# V2 (b): v1's single constant `CAP = 8192` was BOTH the bound
# `validate_arms` enforced on a declared per-arm ceiling AND the default
# an arm that declares none receives.  Only the bound moves.
# `MAX_CEILING` mirrors the provider's own bound - see
# `provider_openai_compat._RecordedCaller._validate_call_args`, which
# refuses any `max_tokens` outside `1 <= n <= 393216` - and
# `DEFAULT_CEILING` keeps v1's value, so an arm that declares nothing is
# settled exactly as v1 settles it.
MAX_CEILING = 393216
DEFAULT_CEILING = 8192
# V3 (c): the wall clock becomes a per-arm declaration.  The bound is the
# transport's own - `Endpoint.__post_init__` and `EndpointSettings`
# both admit 1..600 and refuse 601 - and there is deliberately no default
# constant beside it: an arm that declares no clock takes the endpoint
# record's own value, which is how v2 settles every arm.
MAX_TIMEOUT = 600
VIEWS = ('body', 'commitments', 'both')
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z')
# MULTI (a): an arm name is a directory component in the occurrence AND a
# coordinate component the published importer re-validates with
# `graph_import_h005._SAFE_COMPONENT` = ^[A-Za-z0-9_-]+$ - which, unlike `ID`,
# rejects a dot.  Arm names are therefore checked against the stricter of the
# two wherever an arm arrives unfolded - `at()`, where it comes from a
# coordinate - so a name that this runner accepts can never be refused
# downstream with COORDINATE_COMPONENT_UNSAFE after the calls have been spent.
ARM_COMPONENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z')
ENVELOPE = ('## What to return\nA JSON object carrying "body" and "commitments". '
            'Both are strings and nothing else is required.')
PUBLIC_CONTRACT = ('Return one JSON object with exactly two string fields: "body" and '
                   '"commitments". Write the actual commitments separately; do not copy '
                   'the body into that field as a storage shortcut.')


# --------------------------------------------------------------------------- #
# MULTI (a): provider coupling.  The fork calls                                 #
# `minireason.provider_openai_compat` directly: `Endpoint` / `ENDPOINTS`,       #
# `OpenAICompatProvider(endpoint, records_dir)` and `OfflineProvider(endpoint,  #
# records_dir, script)`, whose `complete(...)` writes the write-once            #
# `call-NNNN.request.json` / `.response.json` records the H005 custody chain    #
# reads.  `EndpointSettings.to_dict()` below reproduces that module's own       #
# recorded settings view exactly and `payload_for` reproduces its request body  #
# exactly, so `decode_contribution` and `read_terminal` compare the runner's    #
# declaration against the provider's record, as in the owner's runner.          #
# --------------------------------------------------------------------------- #

_REGISTRY_OVERRIDE = None


def provider_module():
    return __import__(PROVIDER_MODULE, fromlist=['ENDPOINTS'])


def endpoints():
    """The endpoint registry, name -> Endpoint (24 entries as shipped)."""
    if _REGISTRY_OVERRIDE is not None:
        return _REGISTRY_OVERRIDE
    return dict(provider_module().ENDPOINTS)


def set_registry(registry):
    """Install an explicit registry (a restricted study, or a test); None restores."""
    global _REGISTRY_OVERRIDE
    _REGISTRY_OVERRIDE = None if registry is None else dict(registry)


ENDPOINT_FIELDS = ('name', 'base_url', 'model', 'key_env', 'family', 'chat_path',
                   'native', 'max_concurrency', 'timeout_seconds')


def endpoint_record(endpoint):
    """The publishable, key-free record of one endpoint.

    An endpoint name and family are registry labels, not path components
    (`ollama/gpt-oss-120b`, `ollama-cloud/gpt-oss`), so they are checked for
    being printable non-empty text and nothing more; only arm names, which ARE
    path components, get `ARM_COMPONENT`.  `key_env` is an environment variable
    NAME; no credential value is ever read here, and `write_new` refuses any
    output that contains one.
    """
    record = {}
    for field in ENDPOINT_FIELDS:
        if not hasattr(endpoint, field):
            raise ValueError('ENDPOINT_FIELD_MISSING')
        record[field] = getattr(endpoint, field)
    for name in ('name', 'family', 'base_url', 'model', 'chat_path', 'key_env'):
        value = record[name]
        if not isinstance(value, str) or not value.strip() or any(c < ' ' for c in value):
            raise ValueError('ENDPOINT_FIELD_INVALID')
    if type(record['native']) is not bool:
        raise ValueError('ENDPOINT_NATIVE_INVALID')
    if type(record['max_concurrency']) is not int or not 1 <= record['max_concurrency'] <= 5:
        # The owner set five per key.  An endpoint may ask for less, never more.
        raise ValueError('ENDPOINT_CONCURRENCY_INVALID')
    if type(record['timeout_seconds']) is not int or not 1 <= record['timeout_seconds'] <= 600:
        raise ValueError('ENDPOINT_TIMEOUT_INVALID')
    return record


# MULTI (a): thinking is a per-family wire control.  `provider_openai_compat`
# refuses `thinking=` for any family but `deepseek`, so that is the only family
# on which a `native` arm can be declared; `Endpoint.native` is a different axis
# (Ollama's own `/api/chat`) and never means "supports a thinking mode".
THINKING_WIRE = ('deepseek',)

#: How an occurrence was dispatched.  The provider module records a different
#: `kind` (and an `offline` marker) for the scripted stand-in, and the recorded
#: settings must say which one actually ran.
PROVIDER_MODES = ('live', 'offline')


def provider_kind(record, mode):
    """The `kind` `provider_openai_compat` will stamp on this call's records."""
    if mode == 'offline':
        return 'offline-scripted'
    return 'ollama-native-chat' if record['native'] else 'openai-compat-chat'


@dataclass(frozen=True)
class EndpointSettings:
    """MULTI (a): the owner's DeepSeek-locked `Settings`, opened to the registry.

    `to_dict()` is `provider_openai_compat._RecordedCaller._settings_view` for
    this call, field for field, because that dict is what the provider records
    and what `decode_contribution` compares the record against.
    """
    endpoint: str
    family: str
    model: str
    base_url: str
    chat_path: str
    key_env: str
    native: bool
    max_concurrency: int
    timeout_seconds: int
    mode: str = 'live'
    #: None on a family with no thinking control; False/True on DeepSeek.
    thinking: bool | None = None
    reasoning_effort: str = 'low'
    max_tokens: int = DEFAULT_CEILING             # V2 (b): unchanged at 8192
    temperature: float | None = None
    seed: int | None = None

    def __post_init__(self):
        for name in ('endpoint', 'family', 'model', 'base_url', 'chat_path', 'key_env'):
            if not isinstance(getattr(self, name), str) or not getattr(self, name):
                raise ValueError('INVALID_ENDPOINT_SETTINGS')
        if self.mode not in PROVIDER_MODES or type(self.native) is not bool:
            raise ValueError('INVALID_ENDPOINT_SETTINGS')
        if self.thinking is not None and type(self.thinking) is not bool:
            raise ValueError('Invalid thinking controls')
        if self.thinking is not None and self.family not in THINKING_WIRE:
            raise ValueError('ARM_NATIVE_WIRE_UNKNOWN')
        if self.reasoning_effort not in {'low', 'high', 'max'}:
            raise ValueError('Invalid thinking controls')
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 393216:
            raise ValueError('Invalid completion ceiling')
        if type(self.timeout_seconds) is not int or not 1 <= self.timeout_seconds <= 600:
            raise ValueError('Invalid timeout')
        if self.seed is not None and type(self.seed) is not int:
            raise ValueError('Invalid seed')

    @property
    def response_format(self):
        return {'type': 'json_object'}

    def to_dict(self):
        view = {'kind': provider_kind({'native': self.native}, self.mode),
                'endpoint_name': self.endpoint, 'base_url': self.base_url,
                'chat_path': self.chat_path, 'model': self.model, 'family': self.family,
                'native': self.native, 'key_env': self.key_env,
                'timeout_seconds': self.timeout_seconds,
                'max_concurrency': self.max_concurrency, 'retries': 0,
                'native_reasoning_text_persisted': False,
                'max_tokens': self.max_tokens, 'temperature': self.temperature,
                'seed': self.seed, 'response_format': dict(self.response_format),
                'thinking': self.thinking,
                'reasoning_effort': self.reasoning_effort if self.thinking else None,
                'extra': {}}
        if self.mode == 'offline':
            view['offline'] = True
        return view


def dispatch_kwargs(settings, coordinate):
    """The exact keyword call `provider_openai_compat.complete` is given."""
    return {'response_format': dict(settings.response_format),
            'max_tokens': settings.max_tokens, 'temperature': settings.temperature,
            'seed': settings.seed, 'extra': None, 'thinking': settings.thinking,
            'reasoning_effort': settings.reasoning_effort,
            'coordinate': dict(coordinate)}


def default_provider_factory(endpoint, records):
    module = provider_module()
    return module.OpenAICompatProvider(endpoint, records)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def load(path):
    return json.loads(Path(path).read_bytes())


def utc():
    return datetime.now(timezone.utc).isoformat()


# MULTI (a): the owner's write_new guards one credential, DEEPSEEK_API_KEY.
# A multi-family run holds one key per endpoint family, so the guard reads the
# whole key_env vocabulary.  Values are never stored, only compared.
def key_environment_names():
    names = {'DEEPSEEK_API_KEY'}
    try:
        registry = endpoints()
    except Exception:
        registry = {}
    for endpoint in registry.values():
        name = getattr(endpoint, 'key_env', None)
        if isinstance(name, str) and name:
            names.add(name)
    return sorted(names)


#: MULTI (a): a value shorter than this is not searched for.  The guard is an
#: unbounded substring scan, so a one-character placeholder in a key variable
#: occurs in almost every record by accident and would refuse an unrelated
#: write - including the receipt that resolves an attempt already spent.  No
#: real credential of any endpoint in the registry is this short.
MIN_CREDENTIAL_LENGTH = 16


def write_new(path, value):
    raw = value if isinstance(value, bytes) else encoded(value)
    for name in key_environment_names():                                  # MULTI (a)
        key = os.environ.get(name)
        if key and len(key) >= MIN_CREDENTIAL_LENGTH and key.encode('utf-8') in raw:
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


# MULTI (a): arm declarations ------------------------------------------------ #

def canonical_arm(name):
    """Coordinate-safe spelling of a declared arm name.

    A declaration may be written the way the study brief reads it -
    ``mini_fcl@gpt-oss-120b`` - but the arm is a directory component in the
    occurrence and a coordinate component the published importer re-validates
    against ``^[A-Za-z0-9_-]+$``.  ``@``, ``:``, ``/`` and ``.`` are therefore
    folded to ``_``/``__`` deterministically, and the declared spelling is kept
    in the plan as ``declared_name`` (validated to fold to this same name).

    The ``ARM_COMPONENT`` match below is a post-fold assertion, not the place
    the stricter-of-the-two rule bites: every character ``ID`` admits and
    ``ARM_COMPONENT`` rejects - only ``.`` - has already been folded away here,
    so the two regexes are equivalent at this call site.  The strictness is
    load-bearing in ``at()``, where the arm arrives from a coordinate that was
    never folded.
    """
    if not isinstance(name, str) or not name:
        raise ValueError('ARM_NAME_INVALID')
    folded = name.replace('@', '__')
    for character in (':', '/', '.', ' '):
        folded = folded.replace(character, '_')
    if not ARM_COMPONENT.fullmatch(folded):
        raise ValueError('ARM_NAME_NOT_IMPORT_SAFE')
    return folded


ARM_DECLARED = {'surface', 'kind', 'endpoint'}
ARM_OPTIONAL = {'declared_name', 'max_tokens', 'seed', 'timeout_seconds'}  # V3 (d)


def validate_arms(declared, registry, mode='live'):
    """Freeze one occurrence's arm mapping against the endpoint registry."""
    if not isinstance(declared, dict) or not declared:
        raise ValueError('ARMS_DECLARATION')
    if mode not in PROVIDER_MODES:
        raise ValueError('PROVIDER_MODE')
    arms = {}
    for name, spec in declared.items():
        canonical = canonical_arm(name)
        if canonical in arms:
            raise ValueError('ARM_NAME_COLLISION')
        if (not isinstance(spec, dict) or set(spec) - (ARM_DECLARED | ARM_OPTIONAL)
                or not ARM_DECLARED <= set(spec)):
            raise ValueError('ARM_FIELDS')
        surface, kind, endpoint_name = spec['surface'], spec['kind'], spec['endpoint']
        if surface not in SURFACES or kind not in KINDS:
            raise ValueError('ARM_SURFACE_OR_KIND')
        if kind in BASELINE_KINDS and surface != 'prose':
            # A baseline arm renders `bare_instruction` and no template; it has
            # no commitment surface of its own to declare.
            raise ValueError('ARM_BASELINE_SURFACE')
        if not isinstance(endpoint_name, str) or endpoint_name not in registry:
            raise ValueError('UNKNOWN_ENDPOINT')
        record = endpoint_record(registry[endpoint_name])
        if kind == 'native' and record['family'] not in THINKING_WIRE:
            # `provider_openai_compat` refuses a thinking control on any family
            # but DeepSeek, so a native arm anywhere else would record a control
            # that was never exercised.  Refuse the declaration instead.
            raise ValueError('ARM_NATIVE_WIRE_UNKNOWN')
        # MULTI (h): the completion ceiling and the seed are per-arm plan fields.
        # Ollama honours `seed`; DeepSeek declares none, so it stays null there.
        ceiling = spec.get('max_tokens', DEFAULT_CEILING)   # V2 (b): unchanged
        seed = spec.get('seed')
        # V2 (b): the bound is the provider's own, not 8192.
        if type(ceiling) is not int or not 1 <= ceiling <= MAX_CEILING:
            raise ValueError('ARM_CEILING')
        if seed is not None and (type(seed) is not int or seed < 0):
            raise ValueError('ARM_SEED')
        # V3 (e): the wall clock, read from the arm where it is declared and
        # from the endpoint record otherwise, bounded by the transport's own
        # maximum rather than by a figure this file invents.
        timeout = spec.get('timeout_seconds', record['timeout_seconds'])
        if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT:
            raise ValueError('ARM_TIMEOUT')
        # MULTI (a): `declared_name` is frozen into the plan and hashed into
        # `arms_sha256`, so it is validated like every other arm field: printable
        # non-empty text that folds to the very arm it names.
        declared_name = spec.get('declared_name', name)
        if (not isinstance(declared_name, str) or not declared_name.strip()
                or any(c < ' ' for c in declared_name)):
            raise ValueError('ARM_DECLARED_NAME')
        try:
            folds_to_this_arm = canonical_arm(declared_name) == canonical
        except ValueError:
            folds_to_this_arm = False
        if not folds_to_this_arm:
            raise ValueError('ARM_DECLARED_NAME')
        arms[canonical] = {'surface': surface, 'kind': kind, 'endpoint': endpoint_name,
                           'declared_name': declared_name,
                           'mode': mode, 'max_tokens': ceiling, 'seed': seed}
        # V3 (e): a DECLARED clock is frozen beside the ceiling; an arm that
        # declares none carries no key at all, so a v3 plan built from a v2
        # arms.json is v2's plan in every field but the runner digests.
        if 'timeout_seconds' in spec:
            arms[canonical]['timeout_seconds'] = timeout
    return arms


# MULTI (j): the scope an occurrence is authorised to run ------------------- #

def validate_scope(scope):
    """Freeze one occurrence's authorised problems and cycles, or None.

    A plan whose `max_calls` is the whole material envelope authorises nothing
    by itself; a register that authorises one problem and one cycle needs the
    runner to refuse the rest, not the operator to remember.
    """
    if scope is None:
        return None
    if not isinstance(scope, dict) or set(scope) != {'problems', 'cycles'}:
        raise ValueError('SCOPE_DECLARATION')
    problems, cycles = scope['problems'], scope['cycles']
    if (not isinstance(problems, list) or not problems
            or not isinstance(cycles, list) or not cycles):
        raise ValueError('SCOPE_DECLARATION')
    for problem_id in problems:
        identifier(problem_id)
    for cycle in cycles:
        if type(cycle) is not int or not 1 <= cycle <= 5:
            raise ValueError('SCOPE_DECLARATION')
    return {'problems': sorted(set(problems)), 'cycles': sorted(set(cycles))}


def in_scope(scope, problem_id, cycle):
    """MULTI (j): whether this coordinate's problem and cycle are authorised."""
    if scope is None:
        return True
    return problem_id in scope['problems'] and cycle in scope['cycles']


def call_count(material, arms, scope):
    """MULTI (j): unique provider calls the scope admits (all of them if None)."""
    total = 0
    for problem in material['problems']:
        for cycle in range(1, len(problem['templates']) + 1):
            if not in_scope(scope, problem['id'], cycle):
                continue
            for arm in arms:
                total += len(nodes_for(material, problem, arm, cycle, arms))
    return total


def provider_mode(arms):
    """MULTI (a): the one transport mode this occurrence declares.

    `read_arms` applies one document-level mode to every arm, so the set is a
    singleton today.  A mixed set is refused rather than reduced: the previous
    `sorted(...)[0]` would have reported a mixed occurrence as `live`, which is
    the wrong answer in the one direction that matters.
    """
    modes = {spec['mode'] for spec in arms.values()}
    if len(modes) != 1:
        raise ValueError('PROVIDER_MODE_MIXED')
    return modes.pop()


def read_arms(path):
    """MULTI (a)(j): `(raw bytes, arm mapping, scope)` of one occurrence.

    `set_registry` is the only registry seam.  Every function that needs the
    registry resolves it through `endpoints()`, so a plan, a wave, a request
    and a dispatch can never be built against two different registries - the
    failure that would produce is a custody refusal after the calls are spent.
    """
    raw = Path(path).read_bytes()
    document = json.loads(raw)
    if (not isinstance(document, dict)
            or document.get('schema') != 'minireason.h005.arms.v1'
            or set(document) - {'schema', 'provider', 'arms', 'scope'}):
        raise ValueError('ARMS_SCHEMA')
    mode = document.get('provider', 'live')
    return (raw, validate_arms(document.get('arms'), endpoints(), mode),
            validate_scope(document.get('scope')))


def arm_spec(arms, arm):
    if not isinstance(arms, dict) or arm not in arms:
        raise ValueError('UNKNOWN_ARM')
    return arms[arm]


def is_baseline(arms, arm):
    return arm_spec(arms, arm)['kind'] in BASELINE_KINDS


def settings_for(arm, arms):
    """MULTI (a): built from the arm's endpoint instead of a fixed DeepSeek row."""
    spec = arm_spec(arms, arm)
    registry = endpoints()
    if spec['endpoint'] not in registry:
        raise ValueError('UNKNOWN_ENDPOINT')
    record = endpoint_record(registry[spec['endpoint']])
    thinking = None
    if record['family'] in THINKING_WIRE:
        thinking = spec['kind'] == 'native'
    elif spec['kind'] == 'native':
        raise ValueError('ARM_NATIVE_WIRE_UNKNOWN')
    return EndpointSettings(
        endpoint=record['name'], family=record['family'], model=record['model'],
        base_url=record['base_url'], chat_path=record['chat_path'],
        key_env=record['key_env'], native=record['native'],
        max_concurrency=record['max_concurrency'],
        # V3 (f): the arm's declared clock, or the endpoint record's.
        timeout_seconds=spec.get('timeout_seconds', record['timeout_seconds']),
        mode=spec.get('mode', 'live'), thinking=thinking, reasoning_effort='low',
        # V2 (b): the same unchanged default an undeclared arm receives.
        max_tokens=spec.get('max_tokens', DEFAULT_CEILING), temperature=None,
        seed=spec.get('seed'))


def payload_for(messages, settings):
    """MULTI (a): `provider_openai_compat._RecordedCaller._build_payload`, mirrored.

    The provider hashes and records the body it actually sends; this is the
    runner's independent declaration of the same bytes, and every terminal
    check compares the two.  On a DeepSeek endpoint the result is byte-identical
    to the owner's `payload_for`.
    """
    if settings.native:
        payload = {'model': settings.model, 'messages': messages, 'stream': False,
                   'options': {'num_predict': settings.max_tokens}}
        if settings.temperature is not None:
            payload['options']['temperature'] = settings.temperature
        if settings.seed is not None:
            payload['options']['seed'] = settings.seed
        payload['format'] = 'json'
    else:
        payload = {'model': settings.model, 'messages': messages, 'stream': False,
                   'max_tokens': settings.max_tokens}
        if settings.temperature is not None:
            payload['temperature'] = settings.temperature
        if settings.seed is not None:
            payload['seed'] = settings.seed
        payload['response_format'] = dict(settings.response_format)
    if settings.thinking is not None:
        payload['thinking'] = {'type': 'enabled' if settings.thinking else 'disabled'}
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
    # MULTI (d): a fork study's material is a copy of H005's carrying an extra
    # `study_id`.  The field is optional and validated when present; every
    # other rule below is the owner's, unchanged.
    if 'study_id' in material and not (isinstance(material['study_id'], str)
                                       and ID.fullmatch(material['study_id'])):
        raise ValueError('MATERIAL_STUDY_ID')
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


def manifest_for(tid, template, arms):
    # V2 (c): the manifest's completion ceiling is derived from the arms this
    # occurrence declares instead of from the module constant.  A manifest is
    # per TEMPLATE and shared by every arm, so the derivation is the maximum
    # declared per-arm ceiling: the smallest figure that is a true upper bound
    # for every arm, a pure function of the frozen `arms.json`, and equal to
    # v1's figure whenever every arm sits at `DEFAULT_CEILING`.
    # `validate_arms` has already defaulted and bounded every value.
    ceiling = max(spec['max_tokens'] for spec in arms.values())
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
                       # V2 (c): from the arms' declared ceiling, not the constant.
                       'completion_tokens_per_call': ceiling,
                       'max_completion_tokens': len(nodes) * ceiling},
            'kinds': kinds, 'port_types': port_types, 'stages': stages}


def runtime_pins(repo):
    repo = Path(repo)
    paths = list((repo / 'src' / 'creib').rglob('*.py'))
    paths += [repo / 'src/minireason/provider.py', repo / 'tools/multicycle_language_probe.py']
    return {p.relative_to(repo).as_posix(): sha(p.read_bytes()) for p in sorted(paths)}


def provider_pins(repo):
    """MULTI (e): the multi-provider module and its registry, pinned by hash.

    They are not folded into `runtime_pins`, whose membership rule is the
    owner's and stays byte-identical.  A pin is null while the concurrently
    built module has not landed; an occurrence whose arms all resolve to the
    `offline` family can still be initialized, prepared and audited, and
    `send_wave` refuses a live family whose module is unpinned.
    """
    pins = {}
    for relative in (PROVIDER_MODULE_PATH, ENDPOINT_REGISTRY_PATH):
        path = safe_source(repo, relative)
        pins[relative] = sha(path.read_bytes()) if path.exists() else None
    return pins


def plan_body(repo, raw, material, arms_raw, arms, scope):
    for name, expected in material.get('source_pins', {}).items():
        if sha(safe_source(repo, name).read_bytes()) != expected:
            raise ValueError('SOURCE_PIN_MISMATCH')
    registry = endpoints()
    used = sorted({spec['endpoint'] for spec in arms.values()})
    caps = key_caps(arms)                                                  # MULTI (b)
    keys = sorted(caps)
    body = {'schema': 'minireason.h005.plan.v1', 'material_sha256': sha(raw),
            'helper_sha256': sha(Path(__file__).read_bytes()),
            # MULTI (e): named explicitly by the fork's brief; the fork IS the
            # helper, so the two hashes coincide by construction and a test
            # pins that they do.
            'runner_sha256': sha(Path(__file__).read_bytes()),
            'arms_sha256': sha(arms_raw),                                  # MULTI (e)
            'study_id': material.get('study_id'),                          # MULTI (d)
            'runtime_pins': runtime_pins(repo),
            'provider_pins': provider_pins(repo),                          # MULTI (e)
            'providers': {name: endpoint_record(registry[name]) for name in used},  # MULTI (e)
            'source_pins': material.get('source_pins', {}),
            'arms': arms,                                                  # MULTI (a)
            'scope': scope,                                                 # MULTI (j)
            'provider_mode': provider_mode(arms),                           # MULTI (a)
            # MULTI (h): the completion ceiling is a per-arm plan field, so a
            # family whose reasoning counts against `max_tokens` can be given a
            # different one without touching any other arm.
            # V3 (g): `max_tokens`, `seed` AND the timeout are the arm's own
            # declarations now; an arm that declares no clock still surfaces
            # the endpoint record's, which is what v2 surfaced for every arm.
            'ceilings': {arm: {'max_tokens': settings_for(arm, arms).max_tokens,
                               'timeout_seconds': settings_for(arm, arms).timeout_seconds,
                               'seed': settings_for(arm, arms).seed} for arm in arms},
            'envelope_repairs_declared': list(ENVELOPE_REPAIRS),            # MULTI (g)
            'settings': {arm: settings_for(arm, arms).to_dict() for arm in arms},
            'max_concurrent_requests': MAX_PER_KEY,
            # MULTI (b): at most five per key, and fewer where an endpoint on
            # that credential asks for fewer; the process ceiling is their sum.
            'max_concurrent_requests_per_key_env': caps,
            'max_concurrent_requests_total': sum(caps.values()),
            'key_environment_names': keys,
            'automatic_retries': 0,
            'cycle_definition': 'one complete template invocation',
            'formal_syntax_validation': False,
            'partial_public_continuation': True,
            # MULTI (a): the owner's closed-form `2 + 3 * nodes` assumed two
            # baseline arms and three multi-call arms.  The fork counts the
            # arms it was actually given; on the H005 five it returns 240.
            # MULTI (j): and it counts only what the declared scope admits, so
            # `max_calls` IS the authorisation.  The full envelope of the
            # material stays visible beside it.
            'max_calls': call_count(material, arms, scope),
            'max_calls_envelope': call_count(material, arms, None),
            # V2 (c): the plan's manifest pins carry the per-arm derivation.
            'manifests': {tid: sha(encoded(manifest_for(tid, template, arms)))
                          for tid, template in material['templates'].items()}}
    return body


def initialize(repo, output, material_path, arms_path):
    # MULTI (a)(d)(j): `arms_path` is new; the arm declaration and the scope are
    # frozen into the occurrence beside the material and pinned by `arms_sha256`.
    output = Path(output)
    raw = Path(material_path).read_bytes()
    material = validate_material(json.loads(raw))
    arms_raw, arms, scope = read_arms(arms_path)
    if scope is not None:
        for problem_id in scope['problems']:
            problem_for(material, problem_id)                              # UNKNOWN_PROBLEM
    plan = plan_body(repo, raw, material, arms_raw, arms, scope)
    plan['plan_id'] = digest(plan)
    with tempfile.TemporaryDirectory(prefix='h005-compile-') as temporary:
        for tid, template in material['templates'].items():
            path = Path(temporary) / (tid + '.json')
            write_new(path, manifest_for(tid, template, arms))      # V2 (c)
            compile_manifest(path)
    if output.exists():
        existing = list(output.iterdir())
        if any(p.name not in ('material.json', 'arms.json') for p in existing):   # MULTI (a)
            raise ValueError('OCCURRENCE_EXISTS')
        for name, frozen in (('material.json', raw), ('arms.json', arms_raw)):
            if (output / name).exists() and (output / name).read_bytes() != frozen:
                raise ValueError('MATERIAL_EXISTS_DIFFERENT')
    if not (output / 'material.json').exists():
        write_new(output / 'material.json', raw)
    if not (output / 'arms.json').exists():                                       # MULTI (a)
        write_new(output / 'arms.json', arms_raw)
    for tid, template in material['templates'].items():
        # V2 (c)
        write_new(output / 'manifests' / (tid + '.json'), manifest_for(tid, template, arms))
    write_new(output / 'plan.json', plan)
    return plan


def verify(repo, output):
    output = Path(output)
    raw = (output / 'material.json').read_bytes()
    material = validate_material(json.loads(raw))
    arms_raw, arms, scope = read_arms(output / 'arms.json')                       # MULTI (a)(j)
    expected = plan_body(repo, raw, material, arms_raw, arms, scope)
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
    for name in ('problem', 'node'):
        identifier(coord[name])
    # MULTI (a): arm membership is checked wherever the arm mapping is in hand;
    # here the arm is checked for the shape the occurrence layout and the
    # published importer both require.
    if not isinstance(coord['arm'], str) or not ARM_COMPONENT.fullmatch(coord['arm']):
        raise ValueError('INVALID_COORDINATE')
    if type(coord['cycle']) is not int or not 1 <= coord['cycle'] <= 5:
        raise ValueError('INVALID_COORDINATE')
    identifier(category)
    identifier(suffix)
    return (Path(output) / category / coord['problem'] / coord['arm'] /
            f'cycle{coord["cycle"]:02d}' / (coord['node'] + '.' + suffix))


def provider_dir(output, coord):
    return at(output, 'provider', coord).with_suffix('')


def nodes_for(material, problem, arm, cycle, arms):
    # MULTI (a): `arms` is new; `arm in ARMS` becomes a lookup in the mapping
    # and `arm in BASELINE_ARMS` becomes the arm's declared kind.
    arm_spec(arms, arm)
    if type(cycle) is not int or not 1 <= cycle <= len(problem['templates']):
        raise ValueError('INVALID_TEMPLATE_COORDINATE')
    if is_baseline(arms, arm):
        return [{'id': 'answer', 'instruction': material['bare_instruction'], 'inputs': []}]
    return material['templates'][problem['templates'][cycle - 1]]['nodes']


def final_coordinate(material, problem, arm, cycle, arms):                # MULTI (a)
    return coordinate(problem['id'], arm, cycle,
                      nodes_for(material, problem, arm, cycle, arms)[-1]['id'])


def source_coordinate(material, problem, coord, source, arms):            # MULTI (a)
    if source in ('previous', 'origin'):
        if coord['cycle'] == 1:
            return None
        return final_coordinate(material, problem, coord['arm'],
                                coord['cycle'] - 1 if source == 'previous' else 1, arms)
    return coordinate(coord['problem'], coord['arm'], coord['cycle'], source)


# MULTI (g): the declared `envelope_unwrap` step ---------------------------- #
#
# Ollama cloud accepts `response_format: json_object` but does not enforce it:
# several models return the envelope inside a Markdown code fence, and raw
# control characters inside the JSON strings make a strict `json.loads` raise.
# Under the owner's strict-only decode every such node becomes OPAQUE and the
# commitments the author actually wrote are lost in decoding - exactly the loss
# root's matched-arm review measured on H005.  The fork therefore declares two
# and only two repairs, applied in this order, before the same strict shape
# check: strip ONE outer Markdown fence when the whole trimmed content is a
# single fenced block, and re-parse with `strict=False` so that a raw control
# character inside a string does not fail the parse.
#
# Nothing else is repaired.  No field is reconstructed, a missing `commitments`
# is never invented, the raw public text is stored byte-for-byte in
# `responses/<node>.txt` and hashed into `public_text_sha256`, and every
# artifact still records `envelope_status` OPAQUE when no declared repair
# yields a well-shaped envelope (PROTOCOL.md, "Preserve partial public output,
# malformed envelopes and erroneous formal syntax").  The receipt records which
# repairs were actually applied and whether the owner's strict-only path would
# have succeeded on the raw text, so the OPAQUE rate of a fork occurrence is
# NOT comparable with H005 occurrence-01 - `strict_parse_would_succeed` is.
ENVELOPE_REPAIRS = ('fence_stripped', 'lenient_control_chars')
REPAIR_FIELDS = ('envelope_repairs', 'strict_parse_would_succeed')
FENCE = re.compile(r'\A```[A-Za-z0-9_+.-]*[ \t]*\r?\n?(.*?)\r?\n?[ \t]*```\Z', re.DOTALL)


def strip_one_fence(content):
    """One outer Markdown fence, or the text unchanged."""
    match = FENCE.match(content.strip())
    return (match.group(1), True) if match else (content, False)


def parse_envelope(text, *, lenient):
    """The owner's shape check; `lenient` only relaxes control-character strictness."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('DUPLICATE_JSON_FIELD')
            result[key] = value
        return result
    try:
        envelope = json.loads(text, object_pairs_hook=unique, strict=not lenient)
    except (ValueError, TypeError):
        return None
    if (isinstance(envelope, dict) and set(envelope) == {'body', 'commitments'}
            and all(isinstance(v, str) for v in envelope.values())):
        return envelope
    return None


def envelope_unwrap(content):
    """Return ``(envelope | None, repairs applied, strict_parse_would_succeed)``."""
    strict = parse_envelope(content, lenient=False)
    if strict is not None:
        return strict, [], True
    repairs, candidate = [], content
    candidate, fenced = strip_one_fence(content)
    if fenced:
        repairs.append('fence_stripped')
        parsed = parse_envelope(candidate, lenient=False)
        if parsed is not None:
            return parsed, repairs, False
    parsed = parse_envelope(candidate, lenient=True)
    if parsed is not None:
        return parsed, repairs + ['lenient_control_chars'], False
    return None, [], False


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
    if usage['completion_tokens'] > settings.max_tokens:          # MULTI (h): per-arm ceiling
        raise ValueError('PROVIDER_CAP_EXCEEDED')
    if record.get('reasoning_content_persisted') or record.get('credential_redaction'):
        raise ValueError('PROVIDER_CONTENT_CUSTODY')
    # MULTI (i): hidden reasoning is a custody failure only where the runner
    # actually set a thinking control and set it to disabled - that is, on the
    # DeepSeek family.  Every other family emits reasoning by default and offers
    # no switch, so its presence is recorded (receipt + provider record) and
    # never silently persisted, rather than failing the node.
    if record.get('reasoning_content_present') and settings.thinking is False:
        raise ValueError('PROVIDER_CONTENT_CUSTODY')
    pair = (record.get('status'), record.get('finish_reason'))
    if pair == ('COMPLETE', 'stop'):
        delivery = 'COMPLETE'
    elif pair == ('INCOMPLETE_GENERATION', 'length'):
        delivery = 'PARTIAL'
    else:
        raise ValueError('PROVIDER_NOT_USABLE')
    envelope, repairs, strict_ok = envelope_unwrap(content)          # MULTI (g)
    valid = envelope is not None
    body = envelope['body'] if valid else content
    commitments = envelope['commitments'] if valid else ''
    return {'body': body, 'commitments': commitments, 'delivery_status': delivery,
            'envelope_status': 'AUTHORED' if valid else 'OPAQUE',
            'public_text_sha256': sha(content.encode('utf-8')),
            'body_sha256': sha(body.encode('utf-8')),
            'commitments_sha256': sha(commitments.encode('utf-8')),
            'envelope_repairs': repairs, 'strict_parse_would_succeed': strict_ok}


def authored_artifact(coord, contribution):
    blobs = MemoryBlobs()
    stage = Stage(label(coord), 'h005.authored.v1', (), False)
    submission = Submission(contribution['body'], contribution['commitments'], (), (), (), {})
    aid, body_ref, commitment_ref = _store_artifact(blobs, stage, submission, 0)
    # MULTI (g): the repair bookkeeping is receipt-level provenance; the artifact
    # record keeps exactly the owner's field set so the published importer reads
    # it unchanged.
    return {'schema': 'minireason.h005.artifact.v1', 'coordinate': coord,
            'artifact_id': aid, 'body_ref': body_ref, 'commitments_ref': commitment_ref,
            **{k: v for k, v in contribution.items() if k not in REPAIR_FIELDS}}


def occurrence_arms(output):
    """MULTI (a): the frozen arm mapping of an occurrence, read from its bytes."""
    return read_arms(Path(output) / 'arms.json')[1]


def read_terminal(output, coord, arms=None):
    # MULTI (a): `arms` is new so that `settings_for` can reach the arm's
    # endpoint; when a caller has no mapping in hand it is read back from the
    # occurrence's own frozen `arms.json`.  Every check below is the owner's.
    arms = arms if arms is not None else occurrence_arms(output)
    request = load(at(output, 'requests', coord))
    trace = load(at(output, 'traces', coord))
    attempt = load(at(output, 'attempts', coord))
    receipt = load(at(output, 'responses', coord))
    settings = settings_for(coord['arm'], arms)
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
                # MULTI (g)(i): the declared repairs, the strict-path counterfactual
                # and the reasoning flag are re-derived, never trusted from the receipt.
                or any(receipt.get(f) != contribution[f] for f in REPAIR_FIELDS)
                or receipt.get('reasoning_content_present') != record.get('reasoning_content_present')
                or receipt['usage'] != record['usage']):
            raise ValueError('ARTIFACT_CUSTODY_MISMATCH')
    elif receipt['status'] != 'FAILED':
        raise ValueError('TERMINAL_STATUS_INVALID')
    return receipt


def read_artifact(output, coord, arms=None):                              # MULTI (a)
    if read_terminal(output, coord, arms)['status'] not in ('COMPLETE', 'PARTIAL'):
        raise ValueError('SOURCE_NOT_USABLE')
    return load(at(output, 'artifacts', coord))


def project(source, view, artifact, previous_coord):
    # MULTI: comment only, and this is the whole of it.  UNCHANGED from the
    # owner's runner - the projected view text is what the published importer's
    # brief/label index is read against, so not one character of it moved.
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
    arms = plan['arms']                                                    # MULTI (a)
    spec = arm_spec(arms, coord['arm'])                                    # MULTI (a)
    problem = problem_for(material, coord['problem'])
    nodes = nodes_for(material, problem, coord['arm'], coord['cycle'], arms)
    node = next((n for n in nodes if n['id'] == coord['node']), None)
    if node is None:
        raise ValueError('UNKNOWN_NODE')
    paired_tid = problem['templates'][coord['cycle'] - 1]
    tid = coord['arm'] + '1' if spec['kind'] in BASELINE_KINDS else paired_tid
    bindings = node['inputs']
    if spec['kind'] in BASELINE_KINDS:
        bindings = [{'source': 'previous', 'view': 'both'}]
        if coord['cycle'] > 2:
            bindings.append({'source': 'origin', 'view': 'both'})
    previous_coord = source_coordinate(material, problem, coord, 'previous', arms)
    projections, visible, originals, dependencies, barriers = [], [], {}, {}, {}
    for binding in bindings:
        source = source_coordinate(material, problem, coord, binding['source'], arms)
        artifact = read_artifact(output, source, arms) if source else None
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
        for earlier in nodes_for(material, problem, coord['arm'], coord['cycle'] - 1, arms):
            prior = coordinate(coord['problem'], coord['arm'], coord['cycle'] - 1, earlier['id'])
            barriers[label(prior)] = prior
    for key, prior in barriers.items():
        read_artifact(output, prior, arms)
        dependencies[key] = prior
    projection_records = []
    if spec['kind'] == 'mini':                                             # MULTI (a)
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
    # MULTI (a): the policy text follows the arm's declared surface instead of
    # the literal arm name `mini_fcl`.
    policy = material['formal_instruction'] if spec['surface'] == 'fcl' else material['prose_instruction']
    messages = [{'role': 'system', 'content': material['system'] + '\n\n' + policy + '\n\n' + PUBLIC_CONTRACT},
                {'role': 'user', 'content': brief}]
    trace = {'schema': 'minireason.h005.trace.v1', 'coordinate': coord, 'template_id': tid,
             'paired_template_id': paired_tid, 'rendering': rendering, 'visible_sources': visible,
             'projection_artifacts': projection_records, 'task_artifact': task_record,
             'barrier_dependencies': list(barriers.values()),
             'origin_aliases_previous': coord['cycle'] == 2,
             'original_brief': brief, 'original_brief_sha256': sha(brief.encode('utf-8')),
             'fixture': 'Reconstructed reducer counters are not provider usage.'}
    settings = settings_for(coord['arm'], arms)
    request = {'schema': 'minireason.h005.request.v1', 'coordinate': coord, 'plan_id': plan['plan_id'],
               'template_id': tid, 'paired_template_id': paired_tid, 'messages': messages, 'messages_sha256': digest(messages),
               'provider_payload': payload_for(messages, settings), 'settings': settings.to_dict(),
               'trace_sha256': digest(trace), 'dependencies': list(dependencies.values())}
    return request, trace


def arm_stopped(output, material, problem, arm, through_cycle, arms):     # MULTI (a)
    # One FAILED node ends this arm for the rest of the occurrence: `retries: 0`
    # is the register's, and `ready_coordinates` then returns an empty queue for
    # the arm forever.  `audit` is where that shows up - see PLAN.md.
    failed = False
    for cycle in range(1, through_cycle + 1):
        for node in nodes_for(material, problem, arm, cycle, arms):
            coord = coordinate(problem['id'], arm, cycle, node['id'])
            response = at(output, 'responses', coord)
            if at(output, 'attempts', coord).exists() and not response.exists():
                raise ValueError('UNRESOLVED_ATTEMPT')
            if response.exists() and read_terminal(output, coord, arms)['status'] == 'FAILED':
                failed = True
    return failed


# MULTI (b): concurrency is per credential, and the ceiling is process-wide -- #

#: The owner's authorisation: five requests in flight on one credential.
MAX_PER_KEY = 5


def arm_key_env(arms, arm):
    """The environment variable name whose credential this arm spends.

    Every endpoint names a credential: `endpoint_record` refuses an empty
    `key_env` as ENDPOINT_FIELD_INVALID and `EndpointSettings.__post_init__`
    as INVALID_ENDPOINT_SETTINGS, so there is no unkeyed group to fall back to
    and none is invented here.
    """
    return settings_for(arm, arms).key_env


def key_caps(arms):
    """The in-flight ceiling for each credential this occurrence spends.

    Five is the owner's authorisation; an endpoint may declare `max_concurrency`
    of 1..5 and never more, and the lowest declaration on a credential is the
    ceiling for it - so `plan.json` cannot state an authorisation wider than the
    transport will take, and a wave cannot be built past it.
    """
    registry, caps = endpoints(), {}
    for arm in arms:
        name = arm_spec(arms, arm)['endpoint']
        if name not in registry:
            raise ValueError('UNKNOWN_ENDPOINT')
        record = endpoint_record(registry[name])
        key = record['key_env']
        caps[key] = min(caps.get(key, MAX_PER_KEY), MAX_PER_KEY, record['max_concurrency'])
    return caps


def key_cap(arms, key):
    caps = key_caps(arms)
    if key not in caps:
        raise ValueError('UNKNOWN_KEY_ENVIRONMENT')
    return caps[key]


def wave_capacity(arms):
    return sum(key_caps(arms).values())


# MULTI (b): the gate is a module-level registry keyed by `key_env`, exactly as
# `provider_openai_compat.slots_for` is, and for the same reason.  A semaphore
# built inside one `send_wave` call could never block - wave construction has
# already held that call to `key_cap` per credential - so two `send_wave` calls
# sharing a credential would admit twice the authorisation, each writing attempt
# markers before the provider's own gate is reached; a crash there strands them
# as UNRESOLVED_ATTEMPT on calls that never went out.  One registry per process
# is what makes the ceiling hold across occurrences, and what makes `send-round`
# safe.  Wave construction stays the first line; this is the second.
_GATE_LOCK = threading.Lock()
_GATES = {}


def key_gate(key_env, cap):
    """The semaphore every in-flight call spending `key_env` in this process shares.

    The first caller fixes the ceiling for that credential; a later caller
    asking for a different one is refused rather than quietly widening an
    authorisation already in force, as the provider module refuses it.
    """
    if not isinstance(key_env, str) or not key_env:
        raise ValueError('UNKNOWN_KEY_ENVIRONMENT')
    if type(cap) is not int or not 1 <= cap <= MAX_PER_KEY:
        raise ValueError('CONCURRENCY_LIMIT_INVALID')
    with _GATE_LOCK:
        existing = _GATES.get(key_env)
        if existing is None:
            _GATES[key_env] = (threading.BoundedSemaphore(cap), cap)
            return _GATES[key_env][0]
        gate, limit = existing
        if limit != cap:
            raise ValueError('CONCURRENCY_LIMIT_CONFLICT')
        return gate


def _reset_gates():
    """Test seam only: forget this process's per-key gates."""
    with _GATE_LOCK:
        _GATES.clear()


def ready_coordinates(output, material, problem, cycle, arms, scope):     # MULTI (a)(j)
    # MULTI (j): a coordinate outside the frozen scope is refused, not silently
    # skipped: the register authorises the problems and cycles in `plan['scope']`
    # and nothing else.
    if not in_scope(scope, problem['id'], cycle):
        raise ValueError('SCOPE_EXCLUDED')
    queues, names = [], list(arms)
    for arm in names:
        nodes = nodes_for(material, problem, arm, cycle, arms)
        if arm_stopped(output, material, problem, arm, cycle, arms):
            queues.append([])
            continue
        if cycle > 1:
            previous = [coordinate(problem['id'], arm, cycle - 1, node['id'])
                        for node in nodes_for(material, problem, arm, cycle - 1, arms)]
            if not all(at(output, 'responses', coord).exists() for coord in previous):
                raise ValueError('PREVIOUS_TEMPLATE_NOT_COMPLETE')
        ready = []
        for index, node in enumerate(nodes):
            coord = coordinate(problem['id'], arm, cycle, node['id'])
            if at(output, 'responses', coord).exists():
                continue
            parents = [source_coordinate(material, problem, coord, b['source'], arms) for b in node['inputs']]
            if index == len(nodes) - 1:
                parents += [coordinate(problem['id'], arm, cycle, n['id']) for n in nodes[:index]]
            if all(parent is None or at(output, 'responses', parent).exists() for parent in parents):
                ready.append(coord)
        queues.append(ready)
    # MULTI (b): the owner filled one wave of five by round-robin over the arm
    # queues.  The fork keeps the round-robin and the per-arm fairness, and
    # replaces the single ceiling of five with five per key_env: a wave may
    # carry 5 x (number of distinct keys) coordinates and never more than five
    # that spend the same credential.
    per_key, selected, caps = {}, [], key_caps(arms)
    capacity = sum(caps.values())
    progressed = True
    while len(selected) < capacity and any(queues) and progressed:
        progressed = False
        for arm, queue in zip(names, queues):
            key = arm_key_env(arms, arm)
            if queue and len(selected) < capacity and per_key.get(key, 0) < caps[key]:
                selected.append(queue.pop(0))
                per_key[key] = per_key.get(key, 0) + 1
                progressed = True
    return selected


def wave_path(output, wave_id):
    if not re.fullmatch(r'wave[0-9]{4}', wave_id):
        raise ValueError('INVALID_WAVE_ID')
    return Path(output) / 'waves' / (wave_id + '.json')


def prepare_wave(repo, output, problem_id, cycle):                        # MULTI (a)(j)
    material, plan = verify(repo, output)
    problem = problem_for(material, problem_id)
    selected = ready_coordinates(output, material, problem, cycle,
                                 plan['arms'], plan['scope'])
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
    paths = {output / 'plan.json', output / 'material.json',
             output / 'arms.json',                                         # MULTI (a)
             Path(__file__).resolve(), wave_path(output, wave['wave_id'])}
    paths.update(safe_source(repo, p) for p in {**plan['runtime_pins'], **plan['source_pins']})
    # MULTI (e): the provider module and its endpoint registry are published
    # inputs too whenever the plan pinned them.
    paths.update(safe_source(repo, p) for p, pin in plan['provider_pins'].items() if pin)
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
            read_artifact(output, coord, plan['arms'])
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


# MULTI (c): the publication ref is configurable ----------------------------- #

def upstream_ref(repo):
    """The current branch's upstream, e.g. `origin/claude/project-state-...`."""
    try:
        name = git(repo, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}')
    except Exception as exc:
        raise ValueError('PUBLISH_REF_UNRESOLVED') from exc
    ref = name.decode('utf-8').strip()
    if not ref:
        raise ValueError('PUBLISH_REF_UNRESOLVED')
    return ref


def split_publish_ref(ref):
    """`origin/feature/x` -> (`origin`, `refs/heads/feature/x`)."""
    if not isinstance(ref, str) or '/' not in ref or ref.startswith('/') or ref.endswith('/'):
        raise ValueError('PUBLISH_REF_INVALID')
    remote, branch = ref.split('/', 1)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', remote) or '..' in branch:
        raise ValueError('PUBLISH_REF_INVALID')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', branch):
        raise ValueError('PUBLISH_REF_INVALID')
    return remote, 'refs/heads/' + branch


def check_published(repo, output, wave, publish_ref=None):
    repo = Path(repo).resolve()
    # MULTI (c): `origin`/`refs/heads/main` was hardcoded.  The default is now
    # the current branch's upstream; the byte comparison below is the owner's.
    ref = publish_ref or upstream_ref(repo)
    remote, qualified = split_publish_ref(ref)
    head = git(repo, 'rev-parse', 'HEAD').decode('ascii').strip()
    published = git(repo, 'ls-remote', '--refs', remote, qualified).decode('ascii').split()
    if not published or published[0] != head:
        raise ValueError('PUBLISH_REF_CHANGED')
    for path in required_paths(repo, output, wave):
        name = path.resolve().relative_to(repo).as_posix()
        if git(repo, 'show', head + ':' + name) != path.read_bytes():
            raise ValueError('INPUT_NOT_PUBLISHED')
    return head


def send_wave(repo, output, wave_id, *, provider_factory=None, publication_check=None,
              notify=print, publish_ref=None):
    material, plan = verify(repo, output)
    arms = plan['arms']                                                    # MULTI (a)
    wave = load(wave_path(output, wave_id))
    if wave['wave_id'] != wave_id or wave['plan_id'] != plan['plan_id']:
        raise ValueError('WAVE_PLAN_CHANGED')
    if not in_scope(plan['scope'], wave['problem'], wave['cycle']):        # MULTI (j)
        raise ValueError('SCOPE_EXCLUDED')
    selected = wave['coordinates']
    # MULTI (b): the wave ceiling is per key - `key_cap` each, their sum in all.
    # This is the FIRST line of the per-key ceiling; the process-wide gate below
    # is the second.  A hand-edited wave carrying six coordinates on one
    # credential is refused here, before any attempt marker or provider.
    caps = key_caps(arms)
    groups = {}
    for coord in selected:
        groups.setdefault(arm_key_env(arms, coord['arm']), []).append(coord)
    if (not 1 <= len(selected) <= sum(caps.values())
            or any(key not in caps or len(rows) > caps[key] for key, rows in groups.items())):
        raise ValueError('WAVE_SIZE_INVALID')
    for coord in selected:
        if at(output, 'attempts', coord).exists() or at(output, 'responses', coord).exists():
            raise FileExistsError('NO_REPLAY')
    problem = problem_for(material, wave['problem'])
    if selected != ready_coordinates(output, material, problem, wave['cycle'],
                                     arms, plan['scope']):
        raise ValueError('WAVE_NOT_DEPENDENCY_READY')
    requests = {}
    for coord in selected:
        request, trace = render_node(repo, output, coord, (material, plan))
        if (load(at(output, 'requests', coord)) != request or load(at(output, 'traces', coord)) != trace
                or wave['request_hashes'][label(coord)] != digest(request)):
            raise ValueError('REQUEST_OR_TRACE_CHANGED')
        requests[label(coord)] = request
    head = (publication_check or check_published)(repo, output, wave, publish_ref)
    resolved = endpoints()
    if provider_factory is None:
        # MULTI (a)(b): one credential per key group, and a live occurrence may
        # not be dispatched against an unpinned provider module.
        live = [arm for arm in {c['arm'] for c in selected}
                if settings_for(arm, arms).mode == 'live']
        if live:
            for key in groups:
                if not os.environ.get(key):
                    raise ValueError('KEY_MISSING')
            if not all(plan['provider_pins'].values()):
                raise ValueError('PROVIDER_MODULE_UNPINNED')
    factory = provider_factory or default_provider_factory
    # MULTI (b): process-wide and memoised per `key_env`, so a second `send_wave`
    # running concurrently on the same credential shares this very semaphore.
    gates = {key: key_gate(key, caps[key]) for key in groups}
    def send(coord):
        request = requests[label(coord)]
        settings = settings_for(coord['arm'], arms)
        # V3 (h): the arm's clock is applied to the resolved `Endpoint` value
        # here, by `dataclasses.replace`, so that `endpoints.json` - a pinned
        # published file other plans hash - is never written.  The refusal
        # below ties the value the transport is about to receive to the arm's
        # frozen declaration; the provider then records it, and
        # `decode_contribution` compares that record against `to_dict()`.
        endpoint = replace(resolved[settings.endpoint],
                           timeout_seconds=settings.timeout_seconds)
        if endpoint.timeout_seconds != settings.timeout_seconds:
            raise ValueError('TIMEOUT_NOT_APPLIED')
        # The gate is acquired BEFORE the attempt marker: an attempt is only
        # ever written for a call this process is about to make.
        with gates[arm_key_env(arms, coord['arm'])]:                         # MULTI (b)
            write_new(at(output, 'attempts', coord),
                      {'schema': 'minireason.h005.attempt.v1', 'coordinate': coord,
                       'request_sha256': digest(request), 'published_commit': head,
                       'wave_id': wave_id, 'started_utc': utc(), 'automatic_retry': False})
            failure_type, failure_code = None, None
            try:
                # MULTI (a): `provider_openai_compat`'s own keyword contract.
                provider = factory(endpoint, provider_dir(output, coord))
                provider.complete(request['messages'],
                                  **dispatch_kwargs(settings, {'harness': 'H005', **coord}))
            except Exception as exc:
                failure_type = type(exc).__name__
                # MULTI (k): the provider's own stable code - HTTP_429,
                # KEY_MISSING, TRANSPORT_OR_RESPONSE_ERROR, SECRET_IN_REQUEST.
                # Without it every provider failure reads `ProviderFailure` and
                # a rate limit cannot be told from a key problem without opening
                # the provider records.
                code = getattr(exc, 'code', None)
                failure_code = code if isinstance(code, str) and code else None
        response_path = provider_dir(output, coord) / 'call-0001.response.json'
        provider_request_path = provider_dir(output, coord) / 'call-0001.request.json'
        receipt = {'schema': 'minireason.h005.receipt.v1', 'coordinate': coord,
                   'request_sha256': digest(request), 'finished_utc': utc(), 'status': 'FAILED',
                   'failure_type': failure_type, 'failure_code': failure_code,   # MULTI (k)
                   'envelope_status': None, 'usage': None,
                   'returned_model': None, 'finish_reason': None,
                   # MULTI (g)(i): per-node repair bookkeeping and the reasoning flag.
                   'envelope_repairs': None, 'strict_parse_would_succeed': None,
                   'reasoning_content_present': None,
                   'provider_request_sha256': sha(provider_request_path.read_bytes()) if provider_request_path.exists() else None,
                   'provider_response_sha256': sha(response_path.read_bytes()) if response_path.exists() else None}
        try:
            record = load(response_path)
            receipt.update({'usage': record.get('usage'), 'returned_model': record.get('returned_model'),
                            'finish_reason': record.get('finish_reason'),
                            'reasoning_content_present': record.get('reasoning_content_present')})
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
                            'envelope_repairs': contribution['envelope_repairs'],      # MULTI (g)
                            'strict_parse_would_succeed': contribution['strict_parse_would_succeed'],
                            'artifact_sha256': sha(at(output, 'artifacts', coord).read_bytes())})
        except Exception as exc:
            receipt['validation_failure_type'] = type(exc).__name__
        # MULTI (a): this receipt is what resolves the attempt marker written
        # above.  A refusal here - the credential guard hitting a field, an
        # unserialisable value - would leave a spent call as a permanent
        # UNRESOLVED_ATTEMPT, so a refused receipt is rewritten once in a form
        # carrying coordinates, enums and hashes only, and says why.
        try:
            write_new(at(output, 'responses', coord), receipt)
        except ValueError as refusal:
            receipt = {key: receipt[key] for key in
                       ('schema', 'coordinate', 'request_sha256', 'finished_utc',
                        'provider_request_sha256', 'provider_response_sha256')}
            receipt.update({'status': 'FAILED', 'failure_type': failure_type,
                            'failure_code': failure_code, 'envelope_status': None,
                            'usage': None, 'returned_model': None, 'finish_reason': None,
                            'envelope_repairs': None, 'strict_parse_would_succeed': None,
                            'reasoning_content_present': None,
                            'validation_failure_type': 'RECEIPT_REFUSED'})
            notify(json.dumps({'coordinate': coord, 'receipt_refused': type(refusal).__name__}))
            write_new(at(output, 'responses', coord), receipt)
        notify(json.dumps({'coordinate': coord, 'status': receipt['status'],
                           'envelope_status': receipt['envelope_status'], 'usage': receipt['usage']}))
        return receipt
    results = []
    # One thread per coordinate; the per-key gate, not the pool, is the ceiling.
    with ThreadPoolExecutor(max_workers=max(1, len(selected))) as executor:     # MULTI (b)
        for future in as_completed([executor.submit(send, coord) for coord in selected]):
            results.append(future.result())
    return sorted(results, key=lambda r: label(r['coordinate']))


# MULTI (b): one round over several occurrences, against one published commit #

def pending_wave(output):
    """The one prepared wave of this occurrence that has not been sent, or None.

    `prepare_wave` refuses to build a second wave while an earlier one has a
    coordinate without a receipt (PREPARED_WAVE_PENDING), so there is at most
    one.
    """
    for path in sorted((Path(output) / 'waves').glob('wave*.json')):
        wave = load(path)
        if any(not at(output, 'responses', coord).exists() for coord in wave['coordinates']):
            return wave
    return None


def send_round(repo, outputs, *, provider_factory=None, publication_check=None,
               notify=print, publish_ref=None):
    """Send the prepared wave of each occurrence, concurrently, under the shared gate.

    `check_published` byte-compares the transitive closure of a wave's inputs,
    which includes the previous wave's receipts, so a wave can only be sent
    after its inputs are committed and pushed.  HEAD does not move between
    sends, so one push serves every occurrence prepared against it: prepare a
    wave for each occurrence whose next wave is ready, commit and push ONCE,
    then send them all against that commit.

    Running them together is safe only because the per-key gate above is
    process-wide: occurrences sharing a credential are held to `key_cap` in
    flight BETWEEN them, not `key_cap` each, and occurrences on different
    credentials overlap freely.  Nothing else is relaxed - each occurrence is
    still sent by `send_wave`, with its own publication check, its own wave
    validation and its own NO_REPLAY refusal.
    """
    ordered = [Path(output) for output in outputs]
    if len({path.resolve() for path in ordered}) != len(ordered):
        raise ValueError('OCCURRENCE_REPEATED')
    def drive(output):
        # An occurrence that cannot be verified is an error in its own row, not
        # a quiet "nothing prepared": a mistyped path must not read as done.
        verify(repo, output)
        wave = pending_wave(output)
        if wave is None:
            return {'wave_id': None, 'terminal': 0, 'statuses': []}
        receipts = send_wave(repo, output, wave['wave_id'], provider_factory=provider_factory,
                             publication_check=publication_check, notify=notify,
                             publish_ref=publish_ref)
        return {'wave_id': wave['wave_id'], 'terminal': len(receipts),
                'statuses': [row['status'] for row in receipts]}
    rows = {}
    with ThreadPoolExecutor(max_workers=max(1, len(ordered))) as executor:
        futures = {executor.submit(drive, output): output for output in ordered}
        for future, output in futures.items():
            try:
                rows[output.as_posix()] = future.result()
            except (Exception, KeyboardInterrupt) as exc:
                code = str(exc)
                rows[output.as_posix()] = {
                    'error': code if re.fullmatch('[A-Z0-9_]+', code) else type(exc).__name__}
    return dict(sorted(rows.items()))


def audit(repo, output):
    material, plan = verify(repo, output)
    arms = plan['arms']                                                    # MULTI (a)
    scope = plan['scope']                                                  # MULTI (j)
    counts = {'COMPLETE': 0, 'PARTIAL': 0, 'FAILED': 0, 'OPAQUE': 0,
              # MULTI (g): the comparable figure against H005 occurrence-01.
              'strict_parse_would_succeed': 0, 'fence_stripped': 0,
              'lenient_control_chars': 0, 'reasoning_present': 0,
              'unresolved_attempts': 0, 'unvisited': 0,
              # MULTI (j): anything found outside the authorised scope.
              'out_of_scope': 0}
    usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    unknown_usage, invocations = 0, []
    for problem in material['problems']:
        for arm in arms:
            for cycle in range(1, len(problem['templates']) + 1):
                if not in_scope(scope, problem['id'], cycle):               # MULTI (j)
                    # Nothing outside the register's scope should exist; if it
                    # does, the audit counts it rather than passing over it.
                    for node in nodes_for(material, problem, arm, cycle, arms):
                        coord = coordinate(problem['id'], arm, cycle, node['id'])
                        if (at(output, 'responses', coord).exists()
                                or at(output, 'attempts', coord).exists()):
                            counts['out_of_scope'] += 1
                    continue
                statuses = []
                for node in nodes_for(material, problem, arm, cycle, arms):
                    coord = coordinate(problem['id'], arm, cycle, node['id'])
                    if at(output, 'responses', coord).exists():
                        receipt = read_terminal(output, coord, arms)
                        status = receipt['status']
                        counts[status] += 1
                        if receipt['envelope_status'] == 'OPAQUE':
                            counts['OPAQUE'] += 1
                        if receipt.get('strict_parse_would_succeed'):          # MULTI (g)
                            counts['strict_parse_would_succeed'] += 1
                        for repair in receipt.get('envelope_repairs') or ():
                            counts[repair] += 1
                        if receipt.get('reasoning_content_present'):           # MULTI (i)
                            counts['reasoning_present'] += 1
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
                                    'endpoint': arms[arm]['endpoint'],            # MULTI (a)
                                    'template_id': arm + '1' if is_baseline(arms, arm) else problem['templates'][cycle - 1],
                                    'paired_template_id': problem['templates'][cycle - 1], 'nodes': len(statuses),
                                    'complete': all(s in ('COMPLETE', 'PARTIAL') for s in statuses)})
    return {'plan_id': plan['plan_id'], 'max_calls': plan['max_calls'],
            'scope': scope,                                                # MULTI (j)
            'counts': counts,
            'known_usage': usage, 'unknown_usage_calls': unknown_usage, 'invocations': invocations}


def study_paths(args):
    """MULTI (d): resolve --study/--output/--material/--arms into four paths."""
    study = Path(args.study) if args.study else None
    if study is not None and not study.is_absolute():
        study = Path(args.repo) / study
    output = Path(args.output) if args.output else (study / 'occurrence-01' if study else None)
    if output is None and not getattr(args, 'occurrences', None):          # MULTI (b)
        raise ValueError('OUTPUT_ARGUMENT_REQUIRED')
    material = Path(args.material) if args.material else (study / 'material.json' if study else None)
    # An arm declaration frozen in the occurrence wins over a study-wide one, so
    # a study whose families sit in separate occurrences needs no extra flag.
    arms = Path(args.arms) if args.arms else None
    if arms is None and (output / 'arms.json').exists():
        arms = output / 'arms.json'
    elif arms is None and study is not None:
        arms = study / 'arms.json'
    if study is not None:
        identifier(study.name)
    return study, output, material, arms


def round_outputs(occurrences, study):
    """MULTI (b): `--occurrences` for `send-round`, resolved against the study."""
    if not occurrences:
        raise ValueError('OCCURRENCES_ARGUMENT_REQUIRED')
    outputs = []
    for name in occurrences:
        path = Path(name)
        if not path.is_absolute() and study is not None and not path.exists():
            path = study / name
        outputs.append(path)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('initialize', 'verify', 'prepare-wave',
                                              'send-wave', 'send-round', 'audit'))  # MULTI (b)
    parser.add_argument('--repo', type=Path, default=REPOSITORY)
    parser.add_argument('--study')                                          # MULTI (d)
    parser.add_argument('--output', type=Path)                              # MULTI (d): now optional
    parser.add_argument('--material', type=Path)
    parser.add_argument('--arms', type=Path)                                # MULTI (a)
    parser.add_argument('--publish-ref', dest='publish_ref')                # MULTI (c)
    parser.add_argument('--problem')
    parser.add_argument('--cycle', type=int)
    parser.add_argument('--wave')
    parser.add_argument('--occurrences', nargs='+')                         # MULTI (b)
    args = parser.parse_args()
    prompted = []
    try:
        study, output, material_path, arms_path = study_paths(args)
        if args.operation == 'initialize':
            if material_path is None or arms_path is None:
                raise ValueError('MATERIAL_ARGUMENT_REQUIRED')
            material = validate_material(json.loads(Path(material_path).read_bytes()))
            if study is not None and material.get('study_id') not in (None, study.name):
                raise ValueError('STUDY_ID_MISMATCH')                       # MULTI (d)
            plan = initialize(args.repo, output, material_path, arms_path)
            result = {'plan_id': plan['plan_id'], 'max_calls': plan['max_calls'],
                      'study_id': plan['study_id'], 'arms': sorted(plan['arms'])}
        elif args.operation == 'verify':
            _, plan = verify(args.repo, output)
            result = {'plan_id': plan['plan_id'], 'verified': True}
        elif args.operation == 'prepare-wave':
            result = prepare_wave(args.repo, output, args.problem, args.cycle)
        elif args.operation == 'send-wave':
            if os.environ.get('PROVIDER_KEY_INPUT') == 'prompt':             # MULTI (a)
                if not sys.stdin.isatty():
                    raise ValueError('KEY_PROMPT_REQUIRES_TTY')
                _, plan = verify(args.repo, output)
                wave = load(wave_path(output, args.wave))
                for key in sorted({arm_key_env(plan['arms'], c['arm'])
                                   for c in wave['coordinates']}):
                    if not os.environ.get(key):
                        os.environ[key] = getpass.getpass(key + ': ')
                        prompted.append(key)
            receipts = send_wave(args.repo, output, args.wave, publish_ref=args.publish_ref)
            result = {'wave_id': args.wave, 'terminal': len(receipts),
                      'statuses': [r['status'] for r in receipts]}
        elif args.operation == 'send-round':                                # MULTI (b)
            outputs = round_outputs(args.occurrences, study)
            if os.environ.get('PROVIDER_KEY_INPUT') == 'prompt':
                if not sys.stdin.isatty():
                    raise ValueError('KEY_PROMPT_REQUIRES_TTY')
                keys = set()
                for occurrence in outputs:
                    _, occurrence_plan = verify(args.repo, occurrence)
                    wave = pending_wave(occurrence)
                    keys.update(arm_key_env(occurrence_plan['arms'], c['arm'])
                                for c in (wave or {'coordinates': []})['coordinates'])
                for key in sorted(keys):
                    if not os.environ.get(key):
                        os.environ[key] = getpass.getpass(key + ': ')
                        prompted.append(key)
            result = send_round(args.repo, outputs, publish_ref=args.publish_ref)
        else:
            result = audit(args.repo, output)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        code = str(exc)
        print(json.dumps({'error': code if re.fullmatch('[A-Z0-9_]+', code) else type(exc).__name__}))
        return 2
    finally:
        for key in prompted:
            os.environ.pop(key, None)


if __name__ == '__main__':
    raise SystemExit(main())
