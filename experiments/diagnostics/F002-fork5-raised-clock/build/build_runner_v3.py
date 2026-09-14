"""Build tools/multicycle_commitment_study_multi_v3.py from the published v2.

The v3 file is NOT hand-written: it is v2's bytes with the exact replacements
below and no others, so the diff proof in
`tests/test_multicycle_commitment_study_multi_v3.py` is a statement about what
this script did.  Run it with --check to verify the staged file still matches.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys

V2_SHA256 = '8f7eb9d73e8c497f6a2aabf826a8409bb3c60682b36aaa361f650a9e870adbd0'

DOCSTRING_V3 = '''"""H005 multi-provider fork v3: per-arm wall clock beside the per-arm ceiling.

V3 PROVENANCE.  This file is a byte copy of
``tools/multicycle_commitment_study_multi_v2.py`` at sha256
``{v2}``
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

'''.format(v2=V2_SHA256)

REPLACEMENTS = (
    # (b)
    ("from dataclasses import asdict, dataclass\n",
     "from dataclasses import asdict, dataclass, replace   # V3 (b)\n"),
    # (c)
    ("MAX_CEILING = 393216\nDEFAULT_CEILING = 8192\n",
     "MAX_CEILING = 393216\nDEFAULT_CEILING = 8192\n"
     "# V3 (c): the wall clock becomes a per-arm declaration.  The bound is the\n"
     "# transport's own - `Endpoint.__post_init__` and `EndpointSettings`\n"
     "# both admit 1..600 and refuse 601 - and there is deliberately no default\n"
     "# constant beside it: an arm that declares no clock takes the endpoint\n"
     "# record's own value, which is how v2 settles every arm.\n"
     "MAX_TIMEOUT = 600\n"),
    # (d)
    ("ARM_OPTIONAL = {'declared_name', 'max_tokens', 'seed'}\n",
     "ARM_OPTIONAL = {'declared_name', 'max_tokens', 'seed', 'timeout_seconds'}  # V3 (d)\n"),
    # (e) read and bound
    ("        if seed is not None and (type(seed) is not int or seed < 0):\n"
     "            raise ValueError('ARM_SEED')\n",
     "        if seed is not None and (type(seed) is not int or seed < 0):\n"
     "            raise ValueError('ARM_SEED')\n"
     "        # V3 (e): the wall clock, read from the arm where it is declared and\n"
     "        # from the endpoint record otherwise, bounded by the transport's own\n"
     "        # maximum rather than by a figure this file invents.\n"
     "        timeout = spec.get('timeout_seconds', record['timeout_seconds'])\n"
     "        if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT:\n"
     "            raise ValueError('ARM_TIMEOUT')\n"),
    # (e) freeze
    ("        arms[canonical] = {'surface': surface, 'kind': kind, 'endpoint': endpoint_name,\n"
     "                           'declared_name': declared_name,\n"
     "                           'mode': mode, 'max_tokens': ceiling, 'seed': seed}\n",
     "        arms[canonical] = {'surface': surface, 'kind': kind, 'endpoint': endpoint_name,\n"
     "                           'declared_name': declared_name,\n"
     "                           'mode': mode, 'max_tokens': ceiling, 'seed': seed}\n"
     "        # V3 (e): a DECLARED clock is frozen beside the ceiling; an arm that\n"
     "        # declares none carries no key at all, so a v3 plan built from a v2\n"
     "        # arms.json is v2's plan in every field but the runner digests.\n"
     "        if 'timeout_seconds' in spec:\n"
     "            arms[canonical]['timeout_seconds'] = timeout\n"),
    # (f)
    ("        max_concurrency=record['max_concurrency'], timeout_seconds=record['timeout_seconds'],\n",
     "        max_concurrency=record['max_concurrency'],\n"
     "        # V3 (f): the arm's declared clock, or the endpoint record's.\n"
     "        timeout_seconds=spec.get('timeout_seconds', record['timeout_seconds']),\n"),
    # (g)
    ("            # `max_tokens` and `seed` are the arm's own declarations; the\n"
     "            # timeout is surfaced per arm but READ FROM THE ENDPOINT - it is not\n"
     "            # in ARM_OPTIONAL and no arm declaration can change it.\n",
     "            # V3 (g): `max_tokens`, `seed` AND the timeout are the arm's own\n"
     "            # declarations now; an arm that declares no clock still surfaces\n"
     "            # the endpoint record's, which is what v2 surfaced for every arm.\n"),
    # (h)
    ("        endpoint = resolved[settings.endpoint]\n",
     "        # V3 (h): the arm's clock is applied to the resolved `Endpoint` value\n"
     "        # here, by `dataclasses.replace`, so that `endpoints.json` - a pinned\n"
     "        # published file other plans hash - is never written.  The refusal\n"
     "        # below ties the value the transport is about to receive to the arm's\n"
     "        # frozen declaration; the provider then records it, and\n"
     "        # `decode_contribution` compares that record against `to_dict()`.\n"
     "        endpoint = replace(resolved[settings.endpoint],\n"
     "                           timeout_seconds=settings.timeout_seconds)\n"
     "        if endpoint.timeout_seconds != settings.timeout_seconds:\n"
     "            raise ValueError('TIMEOUT_NOT_APPLIED')\n"),
)


def build(v2_path: Path) -> bytes:
    raw = v2_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != V2_SHA256:
        raise SystemExit('V2 bytes are not the pinned ones: %s' % digest)
    text = raw.decode('utf-8')
    head, sep, tail = text.partition('"""\nfrom __future__ import annotations')
    if not sep:
        raise SystemExit('v2 module docstring not found')
    # (a)+(g of v2): v2's header becomes v3's header with v2's own text beneath.
    v2_doc = head[len('"""H005 multi-provider fork v2: immutable outer DAG across model families.\n'):]
    text = DOCSTRING_V3 + v2_doc.lstrip('\n') + sep + tail
    for old, new in REPLACEMENTS:
        if text.count(old) != 1:
            raise SystemExit('replacement is not unique: %r' % old[:60])
        text = text.replace(old, new)
    return text.encode('utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--v2', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    built = build(args.v2)
    if args.check:
        current = args.out.read_bytes()
        if current != built:
            print('DIFFERS')
            return 1
        print('MATCHES sha256=%s' % hashlib.sha256(built).hexdigest())
        return 0
    args.out.write_bytes(built)
    print('wrote %s sha256=%s' % (args.out, hashlib.sha256(built).hexdigest()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
